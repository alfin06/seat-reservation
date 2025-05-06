<template>
  <div class="auth-form">
    <h2>{{ $t('login') }}</h2>

    <div class="login-tabs">
      <button :class="{ active: loginMode === 'form' }" @click="loginMode = 'form'">
        {{ $t('loginWithCredentials') }}
      </button>
      <button :class="{ active: loginMode === 'qr' }" @click="loginMode = 'qr'">
        {{ $t('loginWithQR') }}
      </button>
    </div>

    <form v-if="loginMode === 'form'" @submit.prevent="handleLogin">
      <div class="form-group">
        <input
          v-model="email"
          type="email"
          :placeholder="$t('emailPlaceholder')"
          required
        />
      </div>
      <div class="form-group">
        <input
          v-model="password"
          type="password"
          :placeholder="$t('password')"
          required
        />
        <div class="forgot-password">
          <router-link to="/forgot-password">{{ $t('forgotPassword') }}</router-link>
        </div>
      </div>
      <button type="submit" class="auth-button">{{ $t('login') }}</button>
    </form>

    <div v-else class="qr-login">
      <p class="qr-instruction">{{ $t('scanQRCodeToLogin') }}</p>
      <div class="qr-box">
        <img :src="qrCodeUrl" alt="QR Code" class="qr-image" />
      </div>
      <p class="qr-note">{{ $t('qrHint') }}</p>
    </div>

    <p class="auth-link">
      {{ $t('dontHaveAccount') }}
      <router-link to="/register">{{ $t('registerHere') }}</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      loginMode: 'form',
      qrCodeUrl: 'https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=login-session-token'
    }
  },
  methods: {
    handleLogin() {
      // Set authentication tokens
      const isAdmin = this.email.includes('admin')
      localStorage.setItem('token', 'valid-token-' + Date.now())
      localStorage.setItem('role', isAdmin ? 'admin' : 'student')
      
      // Force reload to reset application state
      window.location.href = isAdmin ? '/admin' : '/reservation'
    }
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 30px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}

.login-tabs {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.login-tabs button {
  padding: 8px 14px;
  background: #f2f2f2;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s;
}

.login-tabs button.active {
  background-color: #646cff;
  color: white;
  border-color: #646cff;
}

.form-group {
  margin-bottom: 20px;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.auth-button {
  width: 100%;
  padding: 12px;
  background-color: #646cff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.auth-button:hover {
  background-color: #535bf2;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  color: #7f8c8d;
}

.auth-link a {
  color: #646cff;
  text-decoration: none;
  font-weight: 500;
}

.auth-link a:hover {
  text-decoration: underline;
}

.forgot-password {
  text-align: right;
  margin-top: 8px;
}

.forgot-password a {
  color: #646cff;
  font-size: 14px;
  text-decoration: none;
}

.forgot-password a:hover {
  text-decoration: underline;
}

.qr-login {
  text-align: center;
}

.qr-instruction {
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
}

.qr-box {
  display: flex;
  justify-content: center;
  padding: 10px;
}

.qr-image {
  width: 180px;
  height: 180px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.qr-note {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-top: 10px;
}
</style>