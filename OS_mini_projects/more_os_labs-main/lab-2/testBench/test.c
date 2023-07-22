//#include <linux/init.h>
//#include <linux/version.h>
#include <linux/module.h>
#include <linux/kernel.h>
//#include <linux/fs.h>
//#include <linux/miscdevice.h>
//#include <linux/sched.h>
//#include <linux/gfp.h>
//#include <linux/slab.h>
//#include <linux/memory.h>
//#include <linux/mm.h>

struct page *p;

static int test_init(void){
	printk(KERN_INFO "Loaded test\n");
	p = alloc_page(GFP_KERNEL);
	return 0;
}
static void test_exit(void){
	__free_page(p);
	printk(KERN_INFO "Unloaded test\n");
}

module_init(test_init);
module_exit(test_exit);

