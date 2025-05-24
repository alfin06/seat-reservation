<template>
  <el-card class="box-card">
    <h2>{{ $t('register') }}</h2>
    <el-form :model="form" ref="registerForm" label-width="120px" @submit.prevent="onSubmit">
      <el-form-item :label="$t('enterUsername')" prop="username">
        <el-input v-model="form.username" :placeholder="$t('enterUsername')"></el-input>
      </el-form-item>
      <el-form-item :label="$t('enterEmail')" prop="email">
        <el-input v-model="form.email" :placeholder="$t('enterEmail')"></el-input>
      </el-form-item>
      <el-form-item :label="$t('enterPassword')" prop="password">
        <el-input v-model="form.password" type="password" :placeholder="$t('enterPassword')"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">{{ $t('submitRegister') }}</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit() {
      // Handle form submission here (e.g., API call)
      console.log('Register form submitted:', this.form);
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
