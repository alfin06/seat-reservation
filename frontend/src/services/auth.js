export default {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    },
    isAdmin() {
      return localStorage.getItem('role') === 'admin'
    },
    login(token, role) {
      localStorage.setItem('token', token)
      localStorage.setItem('role', role)
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
    },
    getCurrentUser() {
      return {
        token: localStorage.getItem('token'),
        role: localStorage.getItem('role')
      }
    }
  }