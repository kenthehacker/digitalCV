Kenichi Matsuo 

### no.1 Initial Configuration
[751769.623956] Loaded kmod_paging module
[751773.214673] paging_mmap() invoked: new VMA for pid 10760 from VA 0xb6bf1000 to 0xb6dda000
[751773.214706] paging_mmap() invoked: new VMA for pid 10760 from VA 0xb6a08000 to 0xb6bf1000
[751773.214734] paging_mmap() invoked: new VMA for pid 10760 from VA 0xb681f000 to 0xb6a08000
[751773.214772] paging_vma_fault() invoked: took a page fault at VA 0xb681f000
[751773.215176] paging_vma_close() invoked
[751773.215192] paging_vma_close() invoked
[751773.215207] paging_vma_close() invoked
[751780.843130] Unloaded kmod_paging module

new VMA ranges were allocated by the user-space program when it calls mmap()
however, right after that, we see that paging_vma_fault() is invoked, indicating
the user-space program attempted to read/write into the VMA range that was created
if we want to alter memory within the VMA range, we need to use the device file
and have the kernel module communicate indirectly via the device file; only
the kernel module should read/write into the VMA range 

### no.2 Datatype Design

As of now, the following is my struct:

struct page_data{
    atomic_t ref_count;
    void * phys_mem_ptr;
};

the ref_count increments and decrements when the open and close call back functions are ran
i'm assuming i need the phys_mem_ptr which is a generic pointer. as of now, im guessing that
i'll need to store a pointer to pages, this may be updated as i finish parts 3 and 4

### no.3 Page Fault Handler

[ 1181.255744] paging_mmap() invoked: new VMA for pid 14767 from VA 0xb6d5f000 to 0xb6ddf000
[ 1181.255777] paging_mmap() invoked: new VMA for pid 14767 from VA 0xb6cdf000 to 0xb6d5f000
[ 1181.255804] paging_mmap() invoked: new VMA for pid 14767 from VA 0xb6c5f000 to 0xb6cdf000
[ 1182.229613] 0 pages opened for VA: 466a1e2d
[ 1182.229634] 1 pages opened and closed 
[ 1182.229654] paging_vma_close() invoked
[ 1182.229674] 0 pages opened for VA: d3feef37
[ 1182.229688] 1 pages opened and closed 
[ 1182.229705] paging_vma_close() invoked
[ 1182.229723] 0 pages opened for VA: a2b0f090
[ 1182.229737] 1 pages opened and closed 
[ 1182.229753] paging_vma_close() invoked


pages = alloc_page(GFP_KERNEL);
pfn = page_to_pfn(pages);
if (!pages){
    printk("failed to alloc_pages \n");
    return VM_FAULT_OOM;
}

vma = vmf->vma;
fault_address = (unsigned long)vmf->address;
virtual_addy = PAGE_ALIGN(fault_address);
remap_unsuccessful = remap_pfn_range(vma, virtual_addy, pfn, PAGE_SIZE, vma->vm_page_prot);
if (remap_unsuccessful){
    printk("failed to remap \n");
    return do_fault(vma, fault_address);
}else{
    return VM_FAULT_NOPAGE;
}


Above, to get the vaddr all you need to do is get the faulting address
by accessing the vmf's address field. Then we need to align it with page_align
then we feed that to our remap method;
this gets us a success for our dense_mm program

kenpi@kenpi:~/Desktop/lab/more_os_labs/lab-2/user $ sudo ./dense_mm 100
Multiplication done


### no.4 Close Callback
    //homemade ->
    struct page_data * priv_page_data = vma->vm_private_data;
    atomic_dec(&priv_page_data->ref_count);
    printk("%d pages opened for VA: %p\n", atomic_read(&priv_page_data->ref_count), &priv_page_data->phys_mem_ptr);
    if (atomic_read(&priv_page_data->ref_count) == 0){
        printk("%d pages opened and closed \n", atomic_read(&priv_page_data->num_opened));
        if (priv_page_data->phys_mem_ptr){
            //kfree(priv_page_data->phys_mem_ptr);
        }
        kfree(priv_page_data);
    }
    __free_page(pages);
    // <-homemade    
    printk(KERN_INFO "paging_vma_close() invoked\n");

the vma contains a private data field which holds the custom struct that i've made, to free everything i have to free inside out. 
i freed the priv_page_data then freed the pages variable. After this, memory leaks should be taken care of


### no.5 Pre-Paging

before adding prepaging i added a print statement inside of the page fault handler and got this:
kenpi@kenpi:~/Desktop/lab/more_os_labs/lab-2/mod $ dmesg
[242001.704199] Loaded kmod_paging module
[242007.518697] paging_mmap() invoked: new VMA for pid 19821 from VA 0xb6b6e000 to 0xb6d6e000
[242007.518731] paging_mmap() invoked: new VMA for pid 19821 from VA 0xb696e000 to 0xb6b6e000
[242007.518758] paging_mmap() invoked: new VMA for pid 19821 from VA 0xb676e000 to 0xb696e000
[242007.518817] inside of paging VMA fault
[242007.518869] inside of paging VMA fault
[242007.518920] inside of paging VMA fault
[242007.518963] inside of paging VMA fault
[242007.518992] inside of paging VMA fault
[242007.519021] inside of paging VMA fault
[242007.519050] inside of paging VMA fault
[242007.519079] inside of paging VMA fault
[242007.519107] inside of paging VMA fault
[242007.519136] inside of paging VMA fault
[242007.519164] inside of paging VMA fault
[242007.519194] inside of paging VMA fault
...

but after i added the modifications with demand_paging=0 i got this:

148732.507652] Unloaded kmod_paging module
[148740.983467] Loaded kmod_paging module
[148745.079405] inside paging_mmap trying to alloc pages
[148745.079428] size: 81920
[148745.079453] order: 5 page_size: 4096
[148745.079479] paging_mmap() invoked: new VMA for pid 21007 from VA 0xb6de6000 to 0xb6dfa000
[148745.079505] inside paging_mmap trying to alloc pages
[148745.079521] size: 81920
[148745.079540] order: 5 page_size: 4096
[148745.079564] paging_mmap() invoked: new VMA for pid 21007 from VA 0xb6dd2000 to 0xb6de6000
[148745.079588] inside paging_mmap trying to alloc pages
[148745.079603] size: 81920
[148745.079622] order: 5 page_size: 4096
[148745.079645] paging_mmap() invoked: new VMA for pid 21007 from VA 0xb6dbe000 to 0xb6dd2000
[148745.123515] 0 pages opened for VA: 63a2ef69
[148745.123535] 1 pages opened and closed 
[148745.123551] freeing 55cd8465
[148745.123569] paging_vma_close() invoked
[148745.123586] 0 pages opened for VA: f5911342
[148745.123601] 1 pages opened and closed 
[148745.123616] freeing 9f2b09b2
[148745.123631] paging_vma_close() invoked
[148745.124032] 0 pages opened for VA: 9de30d98
[148745.124047] 1 pages opened and closed 
[148745.124062] freeing 42e10cb4
[148745.124077] paging_vma_close() invoked


    if (demand_paging != 1){
        printk("inside paging_mmap trying to alloc pages\n");
        length = vma->vm_end-vma->vm_start;
        printk("size: %lu",length);
        nr_pages = (int)(length/PAGE_SIZE);
        order = my_get_order(nr_pages);
        pages = alloc_pages(GFP_KERNEL, order);
        printk("order: %d page_size: %lu\n",order, PAGE_SIZE);
        if (pages == NULL){
            printk("pages is null\n");
        }

        pfn = page_to_pfn(pages);
        
        remap_unsuccessful = remap_pfn_range(vma, vma->vm_start, pfn, length, vma->vm_page_prot);
        if (remap_unsuccessful){
            printk("Failed to map pages in paging mmap\n");
            return -1;
        }
        
    }

above, if demand paging is disabled, then we figure out how many pages we need 
i did this by calculating nr_pages by finding out the end-start length then we find the order
using the same my_get_order from studio. from this, we can alloc_pages 
using the same remap_pfn_range() from the early part of this lab, i just changed some of the params
if i didnt alloc enough pages, this would trigger a page fault and my backup page fault handler
should be invoked, which shouldn't happen in theory.


### no.6 Experiments

for this, check the PDF that is attached






- Attribution of sources
    google documentations i.e. searching up 'alloc_pages()' documentation and landing on kernel.com
    https://www.kernel.org/doc/gorman/html/understand/understand023.html
    https://linux-kernel-labs.github.io/refs/pull/183/merge/labs/memory_mapping.html

- insights when doing lab
    after about 1 hour of staring at the project when i opened i realised it has to do with userspace
    using the device created to communicate indirectly. 

- approximate amount of time:
    ~15+ hours, mostly spent time trying to understand what's even going on

- suggestions:
    i didn't really understand demand paging very well intially, maybe a slow whiteboard walk through in lecture woud be useful;
    at least for me, this was significantly harder than lab1; maybe break down the lab into 2 parts and have two distinct
    deadlines like we had in 361



