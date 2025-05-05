<template>
  <el-card class="box-card">
    <h2>{{ $t('login') }}</h2>
    <el-form :model="form" ref="loginForm" label-width="120px" @submit.prevent="onSubmit">
      <el-form-item :label="$t('enterEmail')" prop="email">
        <el-input v-model="form.email" :placeholder="$t('enterEmail')"></el-input>
      </el-form-item>
      <el-form-item :label="$t('enterPassword')" prop="password">
        <el-input v-model="form.password" type="password" :placeholder="$t('enterPassword')"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">{{ $t('submitLogin') }}</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>


<script>
export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      error: ''
    }
  },
  methods: {
    async onSubmit() {
      this.error = '';
      try {
        // If your backend expects email as username
        const res = await fetch('http://127.0.0.1:8000/api-token-auth/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.form.email,
            password: this.form.password
          })
        });
        const data = await res.json();
        if (data.token) {
          localStorage.setItem('token', data.token);
          this.$router.push('/reservation'); // Make sure this route matches your router config
        } else {
          this.error = data.non_field_errors ? data.non_field_errors[0] : 'Login failed';
        }
      } catch (e) {
        this.error = 'Network error';
      }
    }
  }
}
</script>


<style scoped>
.box-card {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
}
</style>
