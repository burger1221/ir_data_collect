<template>
  <div>
    <div v-if="scrollTop === 0" style="height: 60px; line-height: 60px; padding-left: 30px; padding-right: 30px; width: 100vw; position: fixed; z-index: 3000">
      <svg-icon icon-class="holo" style="width: 98px; height: 36px; color: #ffffff; vertical-align: middle" />
      <div style="float: right">
        <div :class="windowUrl === '/holo/index' ? 'active': ''" class="holo-navbar-link" style="margin-right: 38px" @click="jump2Index">首页</div>
        <div :class="windowUrl === '/holo/holoTalk' ? 'active': ''" class="holo-navbar-link" style="margin-right: 38px" @click="jump2Talk">定制</div>
        <div :class="windowUrl === '/holo/doc' ? 'active': ''" class="holo-navbar-link" @click="jump2Doc">文档</div>
        <div class="holo-navbar-divider" />
        <el-dropdown size="small" trigger="click">
          <span class="holo-navbar-link">工作台</span>
          <el-dropdown-menu slot="dropdown" class="navbar-dropdown">
            <a href="http://link.holo.ruijie.com.cn/" target="_blank">
              <div class="drop-div">
                <div style="float: left; font-size: 14px;">HOLO LINK</div>
                <div class="blue-div" style="float: left; margin-left: 6px">网络管理</div>
                <div style="clear: both" />
              </div>
            </a>
            <a href="http://demo.holo.ruijie.com.cn/" target="_blank">
              <div class="drop-div">
                <div style="float: left; font-size: 14px;">HOLO DEMO</div>
                <div class="blue-div" style="float: left; margin-left: 6px">售前项目</div>
                <div style="clear: both" />
              </div>
            </a>
            <a href="http://join.holo.ruijie.com.cn/" target="_blank">
              <div class="drop-div">
                <div style="float: left; font-size: 14px;">HOLO JOIN</div>
                <div class="blue-div" style="float: left; margin-left: 6px">开发者中心</div>
                <div style="clear: both" />
              </div>
            </a>
          </el-dropdown-menu>
        </el-dropdown>
        <div class="holo-navbar-divider" />
        <div v-if="logStatus !== 'in'" class="holo-navbar-link" @click="jump2login">登录</div>
        <el-dropdown v-if="logStatus === 'in'" size="small" trigger="click" @command="userCommand" >
          <span class="holo-navbar-link">{{ username }}</span>
          <el-dropdown-menu slot="dropdown" class="navbar-dropdown">
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <div v-if="scrollTop !== 0" style="height: 60px; line-height: 60px; padding-left: 30px; padding-right: 30px; width: 100vw; position: fixed; z-index: 3000; background-color: #FFFFFF; box-shadow:0px 0px 4px 0px rgba(0,0,0,0.1);">
      <svg-icon icon-class="holo" style="width: 98px; height: 36px; color: #333333; vertical-align: middle" />
      <div style="float: right">
        <div :class="windowUrl === '/holo/index' ? 'active': ''" class="holo-navbar-link-gray" style="margin-right: 38px" @click="jump2Index">首页</div>
        <div :class="windowUrl === '/holo/holoTalk' ? 'active': ''" class="holo-navbar-link-gray" style="margin-right: 38px" @click="jump2Talk">定制</div>
        <div :class="windowUrl === '/holo/doc' ? 'active': ''" class="holo-navbar-link-gray" @click="jump2Doc">文档</div>
        <div class="holo-navbar-divider-gray" />
        <el-dropdown size="small" trigger="click">
          <span class="holo-navbar-link-gray">工作台</span>
          <el-dropdown-menu slot="dropdown" class="navbar-dropdown">
            <a href="http://link.holo.ruijie.com.cn/" target="_blank">
              <div class="drop-div">
                <div style="float: left; font-size: 14px;">HOLO LINK</div>
                <div class="blue-div" style="float: left; margin-left: 6px">网络管理</div>
                <div style="clear: both" />
              </div>
            </a>
            <a href="http://demo.holo.ruijie.com.cn/" target="_blank">
              <div class="drop-div">
                <div style="float: left; font-size: 14px;">HOLO DEMO</div>
                <div class="blue-div" style="float: left; margin-left: 6px">售前项目</div>
                <div style="clear: both" />
              </div>
            </a>
            <a href="http://join.holo.ruijie.com.cn/" target="_blank">
              <div class="drop-div">
                <div style="float: left; font-size: 14px;">HOLO JOIN</div>
                <div class="blue-div" style="float: left; margin-left: 6px">开发者中心</div>
                <div style="clear: both" />
              </div>
            </a>
          </el-dropdown-menu>
        </el-dropdown>
        <div class="holo-navbar-divider-gray" />
        <div v-if="logStatus !== 'in'" class="holo-navbar-link-gray" @click="jump2login">登录</div>
        <el-dropdown v-if="logStatus === 'in'" size="small" trigger="click" @command="userCommand" >
          <span class="holo-navbar-link-gray">{{ username }}</span>
          <el-dropdown-menu slot="dropdown" class="navbar-dropdown">
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
export default {
  name: 'Holo',
  data() {
    return {
      styleSet: {},
      scrollTop: 0,
      windowUrl: window.location.href.substring(window.location.href.indexOf('#') + 1),
      username: localStorage.getItem('username'),
      logStatus: localStorage.getItem('logStatus')
      // Cookies.set('holo-token', res.data.token)
      // localStorage.setItem('username', self.loginForm.username)
      // localStorage.setItem('logStatus', 'in')
    }
  },
  watch: {
  },
  mounted: function() {
    window.addEventListener('scroll', this.scrollToTop)
  },
  methods: {
    scrollToTop() {
      this.scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
    },
    jump2login() {
      this.$router.push('/login')
    },
    jump2Talk() {
      this.$router.push('/holo/holoTalk')
      this.windowUrl = '/holo/holoTalk'
    },
    jump2Index() {
      this.$router.push('/holo/index')
      this.windowUrl = '/holo/index'
    },
    jump2Doc() {
      this.$router.push('/holo/doc')
      this.windowUrl = '/holo/doc'
    },
    userCommand(command) {
      if (command === 'logout') {
        this.logout()
      }
    },
    logout() {
      this.$store.dispatch('LogOut').then(() => {
        location.reload() // 为了重新实例化vue-router对象 避免bug
      })
      Cookies.remove('holo-token')
      localStorage.setItem('logStatus', 'out')
    },
    openDemo() {
      this.$message({
        message: 'HOLO Demo正在开发中，敬请期待~',
        offset: 100
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  body::-webkit-scrollbar {
    display: none; //隐藏滚动条
  }
  .holoTalk .ivu-divider-horizontal{
    margin: 12px 0;
  }
  .ivu-input:hover, .ivu-input:focus{
    border-color: #01C1B2;
  }
  .holo-banner{
    width: fit-content;
    height: fit-content;
    position: relative;
    .el-carousel{
      width: 100vw;
      height: 24vw;
    }
    .el-carousel__container{
      height: 100% !important;
      width: 100% !important;
    }
  }
  .navbar-dropdown{
    top: 40px !important;
  }
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
  $holo_green: #01C1B2;
  $holo_green_hover: #01a79a;
  $bg: #FFFFFF;
  $dark_gray:#889aa4;
  $light_gray:#eee;
  .welcome-container{
    height: 100vh;
  }
  .welcome-container{
    background-color: $bg;
    .welcome-navbar{
      width: 100%;
      height: 44px
    }
    .production{
      text-align: center;
    }
    .production_slogan{
      color: #727272;
      font-size: 2em;
      margin-top: 64px;
      margin-bottom: 16px
    }
    .welcome-bottom{
      background-color: #000000;
      height: 227px;
      p{
        font-size: 18px;
        color: $bg;
      }
    }

    /** holo+ v1.0 **/
    .holo-section {
      padding: 64px 0;
      background: #fff;
      &-gray {
        background: #F7F8FA;
      }
      &-title {
        font-size: 36px;
        color: #000000;
        line-height: 50px;
        text-align: center;
        &-sub {
          font-size: 16px;
          color: #161616;
          line-height: 22px;
          text-align: center;
        }
      }
      &-img {
        text-align: center; margin-top: 32px;
        img {
          width: 1240px; margin: 0 auto;
        }
      }
      &-merchant {
        text-align: center; margin-top: 56px; opacity: 0;
        img {
          width: 1240px; margin: 0 auto;
        }
      }
      &-func {
        width: 880px; margin: 48px auto 0;
        .grid-content {
          text-align: center;
          cursor: pointer;
          img {
            width: 190px; margin: 0 auto;
          }
          p {
            font-size: 16px; color: #000;
            span {
              display: block;
              width: 0px;
              margin: 4px auto 0;
              height: 2px;
              background: transparent;
              -webkit-transition: .3s cubic-bezier(.645,.045,.355,1);
              -moz-transition: .3s cubic-bezier(.645,.045,.355,1);
              -o-transition: .3s cubic-bezier(.645,.045,.355,1);
              transition: .3s cubic-bezier(.645,.045,.355,1);
            }
          }
          &.active p {
            color: #01A79A;
            position: relative;
            span {
              width: 120px;
              background: #01A79A;
            }
          }
        }
        &-display {
          width: 1240px; margin: 20px auto 0;
        }
        &-item {
          width: 1240px; border: 1px solid #e5e5e5; box-sizing: border-box;
          // &.active {
          //   animation: change2 .3s ease-in;
          //   -moz-animation: change2 .3s ease-in;
          //   -webkit-animation: change2 .3s ease-in;
          //   -o-animation: change2 .3s ease-in;
          //   opacity: 0;
          //   animation-fill-mode : forwards;
          // }
          .left-content {
            padding: 16px; float: left; width: 500px; box-sizing: border-box; cursor: pointer;
            img {
              width: 469px; height: 480px; display: block;
            }
          }
          .right-content {
            padding: 64px 16px 16px; float: left; width: 738px; box-sizing: border-box; overflow: hidden;
            .title {
              font-size: 36px;
              line-height: 50px;
              color: #161616;
              margin-bottom: 8px;
              .link-anchor { cursor: pointer;}
            }
            .sub-title {
              font-size: 16px;
              line-height: 24px;
              color: #161616;
              span {
                vertical-align: middle;
                &.flag {
                  height: 17px;
                  width: 2px;
                  background: #01A79A;
                  display: inline-block;
                  margin-right: 4px;
                }
              }
              &.link-anchor {cursor: pointer;}
            }
            .content-line {
              font-size: 16px;
              line-height: 24px;
              color: #161616;
              &-func {
                margin-top: 40px;
                margin-bottom: 64px;
                .grid-content {
                  text-align: center;
                }
                img {
                  height: 61px;
                }
              }
            }
            .device-list {
              padding: 16px 0 0;
              img {
                height: 45px;
              }
            }
          }
        }
      }
      .link-concact { vertical-align: middle; padding: 7px 13px; font-size: 12px;}
      &-ready {
        text-align: center; margin-top: 72px; position: relative;
        background: url('/static/image/bg_cooperation_1px.png') repeat-x;
        .img {
          width: 1440px; height: 273px; overflow: hidden; margin: 0 auto;
          float: right;
        }
        .link-experience { position: absolute; top: 168px; left: 50%; margin-left: -103px; width: 206px; text-align: center; border-radius: 23px; font-size: 18px; height: 46px; color: #01C1B2; font-weight: bold;}
        .img-flow { position: absolute; top: 48px; left: 50%; margin-left: -295px; width: 590px;}
      }
      &-link {
        width: 880px; margin: 40px auto 0;
        .grid-content{
          text-align: center;
          p {
            background: #000;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            text-align: center;
            font-size: 18px; color: #fff; margin: 0 auto;
            span {
              padding-top: 22px; display: block; cursor: pointer;
            }
          }
        }
      }
    }

    .holo-section-solution {
      background: rgba(35,47,62,0.55);
      position: relative;
      height: 19.4vw;
      width: 100%;
      &-list {
        width: fit-content;
        margin: auto;
      }
      &-item {
        width: 16vw; height: 19.4vw; float: left; overflow: hidden; position: relative; color: #FFFFFF;
        img {
          -webkit-transition: all .2s;
          -moz-transition: all .2s;
          -o-transition: all .2s;
          transition: all .2s;
        }
        .white-divider{
          height: 2px; width: 50px; background-color: #ffffff; margin: auto; margin-top: 15px;
        }
        &:hover {
          cursor: pointer;
          color: #5AE1EC;
          .white-divider{
            background-color: #5AE1EC;
          }
          img {
            transform: scale(1.1);
            -webkit-transform: scale(1.1);
            -moz-transform: scale(1.1);
            -o-transform: scale(1.1);
          }
        }
      }
    }
  }
  .white-link{
    height: fit-content;
    width: fit-content;
    text-align: center;
    position: absolute;
    margin: auto;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 2000;
  }
  .holo-navbar-link{
    color: #FFFFFF;
    cursor: pointer;
    display: inline-block;
    font-size: 14px;
    outline: none;
  }
  .holo-navbar-link:hover{
    color: #26C6DA;
  }
  .holo-navbar-divider{
    height: 24px;
    width: 1px;
    background-color: #ffffff;
    margin-left: 28px;
    margin-right: 28px;
    display: inline-block;
    position: relative;
    top: 5px;
  }
  .holo-navbar-link-gray{
    color: #333333;
    cursor: pointer;
    display: inline-block;
    font-size: 14px;
    outline: none;
  }
  .holo-navbar-link-gray:hover{
    color: #26C6DA;
  }
  .holo-navbar-divider-gray{
    height: 24px;
    width: 1px;
    background-color: #333333;
    margin-left: 28px;
    margin-right: 28px;
    display: inline-block;
    position: relative;
    top: 5px;
  }
  .active{
    color: #26C6DA
  }
  .blue-div{
    height: 16px;
    line-height: 16px;
    background-color: #D4F4F7;
    color: #00ACC1;
    font-size: 10px;
    border-radius:2px;
    padding: 0px 4px;
    position: relative;
    top: 2px;
  }
  .drop-div{
    padding: 4px 14px;
    cursor: pointer;
    color: rgba(0, 0, 0, 0.5);
  }
  .drop-div:hover{
    background-color: #F9F9F9;
    color: #00ACC1;
  }
</style>
