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
      }
    }
  },
  methods: {
    onSubmit() {
      // Handle login form submission here (e.g., API call)
      console.log('Login form submitted:', this.form);
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
