#include <linux/init.h>
#include <linux/version.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/sched.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/memory.h>
#include <linux/mm.h>

#include <paging.h>

struct page *pages;
static unsigned int demand_paging = 1;
module_param(demand_paging, uint, 0644);

static unsigned int my_get_order(unsigned int value){
    unsigned int shifts = 0;
    if (!value){
        return 0;
    }
    if (!(value & (value - 1))){
        value--;
    }
    while (value > 0) {
        value >>= 1;
        shifts++;
    }
    return shifts;
}

struct page_data{   // HOMEMADE
    atomic_t ref_count;
    atomic_t num_opened;
    struct vm_area_struct * phys_mem_ptr;
};

static int do_fault(struct vm_area_struct * vma, unsigned long fault_address){
    printk(KERN_INFO "paging_vma_fault() invoked: took a page fault at VA 0x%lx\n", fault_address);
    return VM_FAULT_SIGBUS;
}


static vm_fault_t paging_vma_fault(struct vm_fault * vmf)
{
    unsigned long pfn;
    struct vm_area_struct * vma;
    unsigned long fault_address;
    unsigned long virtual_addy;
    int remap_unsuccessful;

    printk("inside of paging VMA fault\n");
    //pages allocation moved to mmap function
    pages = alloc_page(GFP_KERNEL);//this should never run

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
    
}



// OPEN callback
static void paging_vma_open(struct vm_area_struct * vma)
{
    //homemade ->
    struct page_data * priv_page_data = vma->vm_private_data;
    atomic_inc(&priv_page_data->ref_count);
    atomic_inc(&priv_page_data->num_opened);
    
    // <-homemade 
    printk(KERN_INFO "paging_vma_open() invoked\n");
}

static void paging_vma_close(struct vm_area_struct * vma)
{
    //homemade ->
    struct page_data * priv_page_data = vma->vm_private_data;
    atomic_dec(&priv_page_data->ref_count);
    printk("%d pages opened for VA: %p\n", atomic_read(&priv_page_data->ref_count), &priv_page_data->phys_mem_ptr);
    if (atomic_read(&priv_page_data->ref_count) == 0){
        printk("%d pages opened and closed \n", atomic_read(&priv_page_data->num_opened));
        if (priv_page_data->phys_mem_ptr){
            printk("freeing %p\n",priv_page_data->phys_mem_ptr);
            //kfree(priv_page_data->phys_mem_ptr);
        }
        kfree(priv_page_data);
    }
    __free_page(pages);
    // <-homemade    
    printk(KERN_INFO "paging_vma_close() invoked\n");
}

static struct vm_operations_struct paging_vma_ops = 
{
    .fault = paging_vma_fault,
    .open  = paging_vma_open,
    .close = paging_vma_close
};



/* vma is the new virtual address segment for the process */
static int paging_mmap(struct file * filp, struct vm_area_struct * vma)
{
    // HOMEMADE STARTS ->
    int order;
    struct page_data * priv_page_data;
    unsigned long pfn;
    int remap_unsuccessful;
    unsigned long length;
    int nr_pages;

    priv_page_data = kmalloc(sizeof(struct page_data), GFP_KERNEL);
    if (!priv_page_data){
        printk("unable to initalise page_data");
        return -1;
    }
    atomic_set(&priv_page_data->ref_count,1);
    atomic_set(&priv_page_data->num_opened,1);
    priv_page_data->phys_mem_ptr = vma;//vma;

    vma->vm_private_data = priv_page_data;
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

    // <- HOMEMADE ENDS

    /* prevent Linux from mucking with our VMA (expanding it, merging it 
     * with other VMAs, etc.)
     */
    vma->vm_flags |= VM_IO | VM_DONTCOPY | VM_DONTEXPAND | VM_NORESERVE | VM_DONTDUMP | VM_PFNMAP;
    /* setup the vma->vm_ops, so we can catch page faults */
    vma->vm_ops = &paging_vma_ops;

    printk(KERN_INFO "paging_mmap() invoked: new VMA for pid %d from VA 0x%lx to 0x%lx\n", current->pid, vma->vm_start, vma->vm_end);

    return 0;
}

static struct file_operations dev_ops =
{
    .mmap = paging_mmap,
};

static struct miscdevice dev_handle =
{
    .minor = MISC_DYNAMIC_MINOR,
    .name = PAGING_MODULE_NAME,
    .fops = &dev_ops,
};
/*** END device I/O **/

/*** Kernel module initialization and teardown ***/
static int kmod_paging_init(void)
{
    int status;

    /* Create a character device to communicate with user-space via file I/O operations */
    status = misc_register(&dev_handle);
    if (status != 0) {
        printk(KERN_ERR "Failed to register misc. device for module\n");
        return status;
    }

    printk(KERN_INFO "Loaded kmod_paging module\n");

    return 0;
}

static void kmod_paging_exit(void)
{
    /* Deregister our device file */
    misc_deregister(&dev_handle);

    printk(KERN_INFO "Unloaded kmod_paging module\n");
}

module_init(kmod_paging_init);
module_exit(kmod_paging_exit);

/* Misc module info */
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Farnsworth");
MODULE_DESCRIPTION("Demand paging k module");

