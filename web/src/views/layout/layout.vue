<template>
  <div class="welcome-content welcome-container" style="min-width: 1274px;">
    <holo-navbar />
    <div>
      <app-main/>
    </div>
  </div>
</template>

<script>
import HoloNavbar from './components/navbar'
import AppMain from './components/AppMain'
export default {
  name: 'Holo',
  components: {
    HoloNavbar,
    AppMain
  },
  data() {
    return {
      styleSet: {}
    }
  },
  watch: {

  },
  mounted: function() {
    window.addEventListener('scroll', this.scrollToTop)
  },
  methods: {
    // 免费体验
    link2Experience() {
      this.$router.push('/welcome/holoCenter')
    },
    // 联系我们 - 打开qq群
    link2Concact() {
      window.open('//shang.qq.com/wpa/qunwpa?idkey=5363db167106fe772ac01222dec960df2d693082a048295ca93ae783d11676db')
    },
    // 无人售货柜
    link2Rfid() {
      this.$router.push('/welcome/package3')
    },
    // 校园健康
    link2School() {
      this.$router.push('/welcome/package4')
    },
    // 山体滑坡
    link2Mountain() {
      this.$router.push('/welcome/package2')
    },
    // holo link
    link2Link() {
      this.$router.push('/welcome/package5')
    },
    jump2login() {
      this.$router.push('/login')
    },
    // 跳转
    goAnchor(selector) {
      document.getElementById(selector).scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' })
      // let anchor = this.$el.querySelector(selector)
      // let top = document.body.scrollTop || document.documentElement.scrollTop;
      // document.body.scrollTop = anchor.offsetTop; // chrome
      // document.documentElement.scrollTop = anchor.offsetTop; // firefox
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
    /*垂直居中，父元素positon:relative, 子元素position:absolute, margin: auto, 上下左右为0，需要设置长宽*/
    .slogan{
      color: $bg;
      font-size: 2em;
      width: 264px;
      height: 33px;
      margin: auto;
      position: absolute;
      left: 0;
      right: 0;
      top: 220px;
      bottom: 0
    }
    .anchor{
      height: 34px;
      line-height: 34px;
      font-size: 14px;
      width: 150px;
      margin: auto;
      position: absolute;
      left: 0;
      right: 0;
      top: 312px;
      bottom: 0;
      background-color: $bg;
      color: #fff;
      background: #01a79b;
      border-radius:35px;
      text-align: center;
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
    .home-green-btn {
      padding: 10px 17px;
      border-radius: 4px;
      border: 1px solid rgba(0, 0, 0, 0);
      color: #FFFFFF;
      background: #01C1B2;
      font-size: 16px;
      line-height: 1;
      cursor: pointer;
      outline: none;
    }
    .home-white-btn {
      padding: 10px 17px;
      border-radius: 4px;
      border: 1px solid #01C1B2;
      background: #FFFFFF;
      color: #01C1B2;
      font-size: 16px;
      line-height: 1;
      cursor: pointer;
      outline: none;
    }
  }
  .animation-in {
    animation: change 1s ease-in;
    -moz-animation: change 1s ease-in;
    -webkit-animation: change 1s ease-in;
    -o-animation: change 1s ease-in;
    opacity: 0;
    animation-fill-mode : forwards
  }
  @keyframes change {
      from { transform: scale(0.8); opacity: 0.8;}
      to { transform: scale(1); opacity: 1;}
  }
  @keyframes change2 {
      from { transform: scale(0.9) translateY(-5%);  opacity: 0.8;}
      to { transform: scale(1) translateY(0%); opacity: 1;}
  }
  .holo-button{
    width: 160px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    color: #FFFFFF;
    background-color: #00ACC1;
    cursor: pointer;
    font-size: 14px;
    margin: auto;
  }
  .holo-button:hover{
    background-color: rgba(0,172,193,0.8);
  }
  .line3-link{
    font-size: 24px;
    color: rgba(0, 0, 0, 0.87);
    height: 33px;
    line-height: 33px;
    margin-top: 19px;
    margin-bottom: 10px;
    cursor: pointer;
  }
  .line3-link:hover{
    color: #00AFC4;
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
</style>
