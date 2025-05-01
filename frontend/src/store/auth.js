import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => {
    const storedState = localStorage.getItem('authState')
    return storedState
      ? JSON.parse(storedState)
      : {
          user: null,
          isAuthenticated: false,
          error: null
        }
  },
  actions: {
    async setCsrfToken() {
      try {
        const response = await fetch('http://localhost:8000/users/auth/set-csrf-token/', {
          method: 'GET',
          credentials: 'include',
        })
        if (!response.ok) {
          throw new Error('Failed to set CSRF token')
        }
      } catch (error) {
        console.error('Failed to set CSRF token:', error)
        throw error
      }
    },

    async register(userData, router = null) {
      this.error = null
      try {
        // First get CSRF token
        await this.setCsrfToken()

        const response = await fetch('http://localhost:8000/users/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify(userData),
        })
        
        if (!response.ok) {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            const error = await response.json();
            throw new Error(error.error || 'Registration failed');
          } else {
            throw new Error(`Registration failed: ${response.status} ${response.statusText}`);
          }
        }
        
        const data = await response.json()
        
        // After successful registration, automatically log in
        await this.login({
          email: userData.email,
          password: userData.password,
          role: userData.role
        }, router)
      } catch (error) {
        console.error('Registration failed:', error)
        this.error = error.message
        throw error
      }
    },

    async login(credentials, router = null) {
      this.error = null
      try {
        // First get CSRF token
        await this.setCsrfToken()

        const response = await fetch('http://localhost:8000/users/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify(credentials),
        })
        
        if (!response.ok) {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            const error = await response.json();
            throw new Error(error.error || 'Login failed');
          } else {
            throw new Error(`Login failed: ${response.status} ${response.statusText}`);
          }
        }
        
        const data = await response.json()
        this.user = {
          ...data.user,
          role: data.role // Include role in user data
        }
        this.isAuthenticated = true
        localStorage.setItem("token", data.token);
        this.saveState()
        
        if (router) {
          // Redirect based on role
          const route = data.role === 'ADMIN' ? 'admin-dashboard' : 'home'
          await router.push({ name: route })
        }
      } catch (error) {
        console.error('Login failed:', error)
        this.user = null
        this.isAuthenticated = false
        this.error = error.message
        this.saveState()
        throw error
      }
    },

    async logout(router = null) {
      this.error = null
      try {
        // First get CSRF token
        await this.setCsrfToken()

        const response = await fetch('http://localhost:8000/users/auth/logout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
        })
        
        if (!response.ok) {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            const error = await response.json();
            throw new Error(error.error || 'Logout failed');
          } else {
            throw new Error(`Logout failed: ${response.status} ${response.statusText}`);
          }
        }

        // Clear user data and state
        this.user = null
        this.isAuthenticated = false
        this.saveState()
        
        // Clear any stored tokens or session data
        localStorage.removeItem('token')
        localStorage.removeItem('authState')
        
        // Redirect to login page
        if (router) {
          await router.push({ name: 'login' })
        }
      } catch (error) {
        console.error('Logout failed:', error)
        // Still clear local state even if server logout fails
        this.user = null
        this.isAuthenticated = false
        this.error = error.message
        this.saveState()
        localStorage.removeItem('authState')
        
        if (router) {
          await router.push({ name: 'login' })
        }
        throw error
      }
    },

    async resetPassword(email) {
      this.error = null
      try {
        // First get CSRF token
        await this.setCsrfToken()

        const response = await fetch('http://localhost:8000/users/auth/password-reset/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify({ email }),
        })
        
        if (!response.ok) {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            const error = await response.json();
            throw new Error(error.error || 'Password reset request failed');
          } else {
            throw new Error(`Password reset failed: ${response.status} ${response.statusText}`);
          }
        }
        
        return await response.json()
      } catch (error) {
        console.error('Password reset request failed:', error)
        this.error = error.message
        throw error
      }
    },

    async fetchUser() {
      try {
        const response = await fetch('http://localhost:8000/users/auth/user/', {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
        })
        
        if (!response.ok) {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to fetch user');
          } else {
            throw new Error(`Failed to fetch user: ${response.status} ${response.statusText}`);
          }
        }

        const data = await response.json()
        this.user = data
        this.isAuthenticated = true
      } catch (error) {
        console.error('Failed to fetch user:', error)
        this.user = null
        this.isAuthenticated = false
      }
      this.saveState()
    },

    saveState() {
      /*
            We save state to local storage to keep the
            state when the user reloads the page.

            This is a simple way to persist state. For a more robust solution,
            use pinia-persistent-state.
             */
      localStorage.setItem(
        'authState',
        JSON.stringify({
          user: this.user,
          isAuthenticated: this.isAuthenticated,
          error: this.error
        }),
      )
    },
  },
})

export function getCSRFToken() {
  /*
    We get the CSRF token from the cookie to include in our requests.
    This is necessary for CSRF protection in Django.
     */
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  if (!cookieValue) {
    console.warn('CSRF token not found in cookies')
    return ''
  }
  return cookieValue
}