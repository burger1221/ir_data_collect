import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n
import axios from 'axios'
import global_ from './components/Global'
import VueLodash from 'vue-lodash'
import VueClipboard from 'vue-clipboard2'
import Cookies from 'js-cookie'
import ba from 'vue-ba'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import VueLazyload from 'vue-lazyload'

import '@/styles/index.scss' // global css
import '@/styles/theme/index.css' // global css

import App from './App'
import store from './store'
import router from './router'

import '@/icons' // icon
import '@/permission' // permission control

/**
 * This project originally used easy-mock to simulate data,
 * but its official service is very unstable,
 * and you can build your own service if you need it.
 * So here I use Mock.js for local emulation,
 * it will intercept your request, so you won't see the request in the network.
 * If you remove `../mock` it will automatically request easy-mock data.
 */
import '../mock' // simulation data

Vue.use(ElementUI, { locale })
Vue.use(iView)
const options = { name: 'lodash' } // customize the way you want to call it
Vue.use(VueLodash, options) // options is optional
VueClipboard.config.autoSetContainer = true // add this line
Vue.use(VueClipboard)
Vue.use(mavonEditor)
Vue.use(VueLazyload)

Vue.config.productionTip = false
Vue.use(ba, '91a319f8cbe7f4e217887d36c0e9c970')
Vue.use(ba, { siteId: '91a319f8cbe7f4e217887d36c0e9c970' })

Vue.prototype.$axios = axios
axios.interceptors.response.use(
  response => {
    if (response.data.code === 10010 || response.data.code === 10011) {
      Cookies.remove('holo-token') // 删除已经失效或过期的token（不删除也可以，因为登录后覆盖）
      router.push({ path: '/login' })
    } else { // 判断token是否存在，如果存在说明需要更新token
      const data = Cookies.get('holo-token')
      if (data != null && data !== '') {
        const token = data
        Cookies.set('holo-token', token)
        return response
      }
    }
    return response
  }, error => {
    // 对响应错误做点什么
    console.log(router)
    if (error.response.status === 401) {
      if (window.location.hash === '#/login') {
        localStorage.setItem('logStatus', 'out')
      } else if (Cookies.get('holo-token') !== undefined || Cookies.get('holo-token') !== null) {
        localStorage.setItem('logStatus', 'out')
        Cookies.remove('holo-token') // 删除已经失效或过期的token（不删除也可以，因为登录后覆盖）
        router.push({ path: '/login' })
        alert('认证已超时，请重新登录')
      } else {
        localStorage.setItem('logStatus', 'out')
        router.push({ path: '/login' })
      }
    }
    return Promise.reject(error)
  })

axios.interceptors.request.use(function(config) { // 每次请求时会从Cookies中获取token
  const data = Cookies.get('holo-token')
  if (data === null || data === 'null' || data === '' || data === undefined) {
    return config
  } else {
    config.headers.Authorization = 'Bearer ' + data
  }
  return config
}, function(error) {
  return Promise.reject(error)
})

Vue.prototype.GLOBAL = global_

// router.afterEach((to, from, next) => {
//   setTimeout(() => {
//     var _hmt = _hmt || [];
//     (function() {
//       // 每次执行前，先移除上次插入的代码
//       document.getElementById('baidu_tj') && document.getElementById('baidu_tj').remove()
//       var hm = document.createElement('script')
//       hm.src = 'https://hm.baidu.com/hm.js?91a319f8cbe7f4e217887d36c0e9c970'
//       hm.id = 'baidu_tj'
//       var s = document.getElementsByTagName('script')[0]
//       s.parentNode.insertBefore(hm, s)
//     })()
//   }, 0)
// })

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
