#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs_struct.h>
#include <linux/fdtable.h>
#include <linux/nsproxy.h>
#include <linux/kthread.h>
#include <linux/path.h>
#include <linux/mount.h>

static struct task_struct * kthread = NULL;

static int thread_fn(void * data){
    struct path pwd_path;
    struct path root_path;
    struct vfsmount *pwd_mnt;
    struct vfsmount *root_mnt;
    struct dentry *pwd_dentry;
    struct dentry *root_dentry;
    struct dentry *curr_dentry;
    
    printk(KERN_INFO "fs: %p files: %p nsproxy: %p \n", current->fs, current->files, current->nsproxy);

    pwd_path = current->fs->pwd;
    root_path = current->fs->root;

    pwd_mnt = pwd_path.mnt;
    root_mnt = root_path.mnt;

    pwd_dentry = pwd_path.dentry;
    root_dentry = root_path.dentry;
    
    printk(KERN_INFO "pwd dentry: %p | root dentry: %p \n", pwd_dentry, root_dentry);
    
    if (pwd_dentry == root_dentry){
        printk(KERN_INFO "pwd and root not the same pwd: %s | root: %s \n", pwd_dentry->d_iname, root_dentry->d_iname);
    }else{
        printk(KERN_INFO "pwd and root were the same %s \n",pwd_dentry->d_iname);
    }

    printk(KERN_INFO "printing curr dir items \n");
    list_for_each_entry(curr_dentry, &(root_dentry->d_subdirs), d_child){
        if (!list_empty(&curr_dentry->d_subdirs)){
            printk("%s\n",curr_dentry->d_iname);
        }
    }
    /*
    list_for_each_entry(f, &fox_list, list) {
    }
    */

    
    while(!kthread_should_stop()){
        //do nothing
    }
    return 0;
}


static int k_mod_init(void){
    printk(KERN_INFO "LOADED studio 15 module \n");
    kthread = kthread_create(thread_fn, NULL, "vfs_kthread");
    wake_up_process(kthread);
    return 0;
}

static void k_mod_exit(void){
    kthread_stop(kthread);
    printk(KERN_INFO "UNLOADED studio 15 module \n");
}

module_init(k_mod_init);
module_exit(k_mod_exit);
MODULE_AUTHOR("Zoidberg");
