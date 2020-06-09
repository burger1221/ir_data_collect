import request from '@/utils/request'

export function login(username, password) {
  const params = {
    'username': username,
    'password': password
  }
  this.$axios.post('/api/auth', JSON.stringify(params))
    .then((res) => {
      return res
    })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}
