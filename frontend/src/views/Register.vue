<template>
  <div class="auth-form">
    <h2>{{ $t('register') }}</h2>
    <form @submit.prevent="handleRegister">
      <!-- Full Name -->
      <div class="form-group">
        <label>{{ $t('fullName') }}</label>
        <input
          v-model="form.name"
          type="text"
          :placeholder="$t('fullNamePlaceholder')"
          required
        />
      </div>

      <!-- Email -->
      <div class="form-group">
        <label>{{ $t('email') }}</label>
        <input
          v-model="form.email"
          type="email"
          :placeholder="$t('emailPlaceholder')"
          required
        />
      </div>

      <!-- Password -->
      <div class="form-group">
        <label>{{ $t('password') }}</label>
        <input
          v-model="form.password"
          type="password"
          :placeholder="$t('passwordPlaceholder')"
          required
        />
        <small class="hint">{{ $t('passwordHint') }}</small>
      </div>

      <!-- Confirm Password -->
      <div class="form-group">
        <label>{{ $t('confirmPassword') }}</label>
        <input
          v-model="form.confirm_password"
          type="password"
          :placeholder="$t('confirmPasswordPlaceholder')"
          required
        />
      </div>

      <!-- Role Selection -->
      <div class="form-group">
        <label>{{ $t('role') }}</label>
        <div class="role-options">
          <label>
            <input
              type="radio"
              v-model="form.role"
              value="STUDENT"
              checked
            />
            <span class="radio-label">{{ $t('student') }}</span>
          </label>
          <label>
            <input
              type="radio"
              v-model="form.role"
              value="ADMIN"
            />
            <span class="radio-label">{{ $t('admin') }}</span>
          </label>
        </div>
      </div>

      <!-- Math CAPTCHA -->
      <div class="form-group">
        <label>{{ $t('captchaQuestion') }}: <strong>{{ mathCaptcha.question }}</strong></label>
        <input
          v-model.number="form.captchaAnswer"
          type="number"
          :placeholder="$t('captchaAnswerPlaceholder')"
          required
        />
      </div>

      <!-- Submit -->
      <button type="submit" class="auth-button">
        {{ $t('register') }}
      </button>
    </form>

    <p class="auth-link">
      {{ $t('alreadyHaveAccount') }}
      <router-link to="/login">{{ $t('loginHere') }}</router-link>
      <span style="margin: 0 5px">•</span>
      <router-link to="/forgot-password">{{ $t('forgotPassword') }}</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        confirm_password: '',
        role: 'STUDENT',
        captchaAnswer: null
      },
      mathCaptcha: {
        question: '',
        answer: null
      }
    }
  },
  created() {
    this.generateMathCaptcha()
  },
  methods: {
    generateMathCaptcha() {
      const a = Math.floor(Math.random() * 10) + 1
      const b = Math.floor(Math.random() * 10) + 1
      this.mathCaptcha.question = `${a} + ${b}`
      this.mathCaptcha.answer = a + b
    },
    handleRegister() {
      if (this.form.password !== this.form.confirm_password) {
        alert(this.$t('passwordMismatch'))
        return
      }

      if (this.form.captchaAnswer !== this.mathCaptcha.answer) {
        alert(this.$t('captchaInvalid'))
        this.generateMathCaptcha()
        this.form.captchaAnswer = null
        return
      }

      // Registration logic here
      console.log('Form submitted:', this.form)
    }
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 30px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

input[type="text"],
input[type="email"],
input[type="password"],
input[type="number"] {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.hint {
  display: block;
  margin-top: 5px;
  color: #7f8c8d;
  font-size: 0.85rem;
}

.role-options {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.role-options label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
}

.radio-label {
  position: relative;
  top: -1px;
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
  margin-top: 10px;
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
</style>
