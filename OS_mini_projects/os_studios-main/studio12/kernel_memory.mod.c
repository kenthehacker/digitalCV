#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xbadffb04, "module_layout" },
	{ 0x7bd61166, "param_ops_uint" },
	{ 0x23196a6c, "kthread_stop" },
	{ 0xbf8d9e8a, "wake_up_process" },
	{ 0xfe6f205b, "kthread_create_on_node" },
	{ 0x316225ce, "__free_pages" },
	{ 0xc5850110, "printk" },
	{ 0x987c11c7, "__pv_phys_pfn_offset" },
	{ 0x5015cc7f, "mem_map" },
	{ 0xb3f7646e, "kthread_should_stop" },
	{ 0x1000e51, "schedule" },
	{ 0xbef6bae2, "__alloc_pages_nodemask" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "9B72E5104E6752C96ECD3CA");
