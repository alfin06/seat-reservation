<script>
import {useAuthStore} from '../store/auth'

export default {
    setup() {
        const authStore = useAuthStore()
        return {
            authStore
        }
    },
    data() {
        return {
            email: "",
            password: "",
            error: ""
        }
    },
    methods: {
        async login() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if(!emailRegex.test(this.email)) {
                this.error = "Invalid email address!"
            }
            else {
                await this.authStore.login(this.email, this.password, this.$router)
                if (!this.authStore.isAuthenticated) {
                    this.error = 'Login failed. Please check your credentials.'
                }
            }
        },
        resetError() {
            this.error = ""
        }
    }
} 
</script>

<template>
    <el-card class="box-card">
        <h2>{{ $t('login') }}</h2>
        <p v-if="error" class="error">{{ error }}</p>
        <el-form :model="form" ref="loginForm" label-width="120px" @submit.prevent="login">
            <el-form-item :label="$t('enterEmail')" prop="email">
                <el-input v-model="email" id="email" type="text" required @input="resetError" :placeholder="$t('enterEmail')"></el-input>
            </el-form-item>
            <el-form-item :label="$t('enterPassword')" prop="password">
                <el-input v-model="password" id="password" type="password" required @input="resetError" :placeholder="$t('enterPassword')"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="login">{{ $t('submitLogin') }}</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>

<style scoped>
.box-card {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
}
</style>