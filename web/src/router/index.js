import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)
/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in subMenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if false, the item will hidden in breadcrumb(default is true)
  }
**/

export const constantRouterMap = [
  { path: '/',
    redirect: {
      path: '/index'
    },
    hidden: true
  },
  // { path: '/welcome', component: () => import('@/views/welcome/welcome'), hidden: true },
  // { path: '/index', component: resolve => require(['@/views/holo/holo'], resolve), hidden: true },
  { path: '/login', component: resolve => require(['@/views/login/login'], resolve), hidden: true },
  { path: '/404', component: resolve => require(['@/views/404'], resolve), hidden: true },
  { path: '/index', component: resolve => require(['@/views/index/index'], resolve), hidden: true },
  { path: '/sign', component: resolve => require(['@/views/index/sign'], resolve), hidden: true },
  // { path: '/holoTalk', component: resolve => require(['@/views/holoTalk/holoTalk'], resolve), hidden: true },
  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
// mode: 'history'
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
