<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style rel="stylesheet/scss" lang="scss">
  /*定义滚动条高宽及背景 高宽分别对应横竖滚动条的尺寸*/
  ::-webkit-scrollbar
  {
    width: 6px;  /*滚动条宽度*/
    height: 6px;  /*滚动条高度*/
  }

  /*定义滚动条轨道 内阴影+圆角*/
  ::-webkit-scrollbar-track
  {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0);
    border-radius: 6px;  /*滚动条的背景区域的圆角*/
    background-color: #FFFFFF;/*滚动条的背景颜色*/
  }

  /*定义滑块 内阴影+圆角*/
  ::-webkit-scrollbar-thumb
  {
    border-radius: 6px;  /*滚动条的圆角*/
    -webkit-box-shadow: inset 0 0 2px rgba(0,0,0,0);
    background-color: rgba(238,238,238,1);  /*滚动条的背景颜色*/
  }
</style>
