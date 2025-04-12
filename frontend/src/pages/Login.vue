<script>
import {useAuthStore} from '../store/auth';

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
                    this.error = this.authStore.message
                }
            }
        },
        resetError() {
            this.error = ""
        },
        onRegister() {
            // For example, redirect to the login page.
            this.$router.push('/register');
        }
    }
} 
</script>

<template>
    <el-card class="box-card card-body">
        <loading v-model:active="isLoading"
                :can-cancel="true"
                :on-cancel="onCancel"
                :is-full-page="fullPage" />
        <h2>{{ $t('login') }}</h2>
        <br/>
        <p v-if="error" class="error">{{ error }}</p>
        <el-form :model="form" ref="loginForm" label-width="120px" @submit.prevent="login" class="form-horizontal form-material">
            <el-form-item :label="$t('enterEmail')" prop="email" class="form-label">
                <el-input v-model="email" id="email" type="text" required @input="resetError" :placeholder="$t('enterEmail')"></el-input>
            </el-form-item>
            <el-form-item :label="$t('enterPassword')" prop="password" class="form-label">
                <el-input v-model="password" id="password" type="password" required @input="resetError" :placeholder="$t('enterPassword')"></el-input>
            </el-form-item>
            <br/>
            <el-form-item>
                <el-button type="primary" @click="login">{{ $t('submitLogin') }}</el-button>
            </el-form-item>
        </el-form>
        <p>{{ $t('noAccount') }}? <el-link @click="onRegister">{{ $t('register') }}</el-link></p>
        <el-link @click="onRegister">{{ $t('forgetPassword') }}?</el-link>
    </el-card>
</template>

<style scoped>
.box-card {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
}
</style>