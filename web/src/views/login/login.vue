<template>
  <div class="login-container">
    <div style="position: absolute; top: 22px; left: 30px">
      <svg-icon icon-class="ruijie" style="height: 50px; width: 125px" />
    </div>
    <span style="position: absolute; font-size: 12px; color: #707070; bottom: 12px; left: 0; right: 0">
      版权所有©2000-2020 锐捷网络股份有限公司 京ICP备13025710号-1 京公网安备11010802020367号
    </span>
    <div style="width: 880px; box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.2); border-radius:16px;">
      <el-row>
        <el-col
          :span="12"
          style="background-image: url('/static/image/loginBG2.png');
          background-repeat: no-repeat;
          background-size: 100% 100%;
          -moz-background-size: 100% 100%;
          border-top-left-radius: 16px;
          border-bottom-left-radius: 16px;
          height: 566px;
          display: flex;
          align-items: center;
          justify-content: center">
          <div style="text-align: center">
            <div style="font-size: 36px; color: #FFFFFF; margin-bottom: 1em">疫情就是命令</div>
            <div style="font-size: 36px; color: #FFFFFF">防控就是责任</div>
          </div>
        </el-col>
        <el-col :span="12" style="background-color: #FFFFFF; border-top-right-radius: 16px; border-bottom-right-radius: 16px;">
          <div style="height: 566px; display: flex; align-items: center; justify-content: center">
            <div>
              <div class="login-title">锐捷园区AI防疫布控解决方案</div>
              <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
                <el-form-item prop="username">
                  <el-input
                    v-model="loginForm.username"
                    name="username"
                    placeholder="请输入用户名"
                    prefix-icon="el-icon-user"
                    @keyup.enter.native="handleLogin"/>
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    :type="pwdType"
                    v-model="loginForm.password"
                    name="password"
                    placeholder="请输入密码"
                    prefix-icon="el-icon-lock"
                    @keyup.enter.native="handleLogin" />
                  <span class="show-pwd" @click="showPwd">
                    <svg-icon :icon-class="pwdType === 'password' ? 'eye' : 'eye-open'" />
                  </span>
                </el-form-item>
                <el-form-item style="text-align: center">
                  <el-button v-track-event.click="{category:'登录', action:'click',opt_label: '登录'}" :loading="loading" type="primary" style="width:100%;" @click.native.prevent="handleLogin">
                    登&nbsp;&nbsp;&nbsp;录
                  </el-button>
                </el-form-item>
                <div style="width: 100%; text-align: left">
                  <span class="click-span">忘记密码</span>
                </div>
              </el-form>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import Cookies from 'js-cookie'

export default {
  name: 'Login',
  data() {
    return {
      canSend: true,
      timeTest: new Date(new Date().getTime() + 1000 * 60),
      canSend2: true,
      timeTest2: new Date(new Date().getTime() + 1000 * 60),
      initalIndex: 0,
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
        password: [{ required: true, message: '密码不能为空', trigger: 'blur' }]
      },
      loading: false,
      pwdType: 'password',
      redirect: undefined,
      showModal: false,
      authcode: ''
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  mounted: function() {
    const self = this
    const query = self.$route.query
    if (query && query.register) {
      self.initalIndex = 1
    }
  },
  methods: {
    showPwd() {
      if (this.pwdType === 'password') {
        this.pwdType = ''
      } else {
        this.pwdType = 'password'
      }
    },
    handleLogin() {
      const self = this
      this.loading = true
      const params = this.loginForm
      this.$axios.defaults.headers['Content-Type'] = 'application/json;charset=UTF-8'
      this.$axios.post('/api/auth', JSON.stringify(params))
        .then((res) => {
          Cookies.set('holo-token', res.data.token)
          localStorage.setItem('username', res.data.userName || self.loginForm.username)
          localStorage.setItem('logStatus', 'in')
          self.$router.push('/')
          this.loading = false
        }).catch(error => {
          this.$Message.error('用户名或密码错误')
          localStorage.removeItem('token')
          console.log(error)
          this.loading = false
        })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
@import "../../styles/baseColor";
$bg:#2d3a4b;
$light_gray:#eee;
$holo_green: #01C1B2;
$holo_green_hover: #01a79a;

/* reset element-ui css */
.login-container {
  background-image: url("/static/image/loginBG.png");
  width: 100%;
  background-repeat: no-repeat;
  background-size: 100% 100%;
  -moz-background-size: 100% 100%;
  position: relative;
  display: -webkit-box;
  -webkit-box-pack:center;
  -webkit-box-align:center;
  -webkit-box-orient: vertical;
  text-align: center;
  .el-form-item{
    margin-bottom: 16px;
  }
  .el-form-item__error{
    z-index: 10;
  }
  .el-carousel__container{
    height: 566px;
  }
}
.register-form{
  .el-form-item{
    margin-bottom: 8px;
  }
}

</style>

<style rel="stylesheet/scss" lang="scss" scoped>
@import "../../styles/baseColor";
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;
.login-title{
  color: $base-color;
  font-size: 22px;
  margin-bottom: 16px;
}
.slogan{
  color: #FFFFFF;
  p{
    text-align: left;
  }
}
.click-span{
  color: $dark_gray;
  cursor: pointer;
}
.login-container {
  position: relative;
  height: 100%;
  width: 100%;
  .login-form {
    margin: auto;
    width: 280px;
    height: fit-content;
    max-width: 100%;
  }
  .svg-container {
    padding: 6px 5px 6px 15px;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }
  .title {
    font-size: 26px;
    font-weight: 400;
    color: $light_gray;
    margin: 0px auto 40px auto;
    text-align: center;
    font-weight: bold;
  }
  .show-pwd {
    position: absolute;
    right: 12px;
    top: 0;
    font-size: 14px;
    cursor: pointer;
    user-select: none;
  }
}
</style>
