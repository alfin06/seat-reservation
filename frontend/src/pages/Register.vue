<script>
import {getCSRFToken} from '../store/auth'

export default {
    data() {
        return {
            email: '',
            password: '',
            password2: '',
            error: '',
            success: ''
        }
    },
    methods: {
        async register() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
            try {
                if(!emailRegex.test(this.email)) {
                    this.error = "Invalid email address!"
                }
                else if (this.password != this.password2) {
                    this.error = "Passwords do not match!"
                }
                else {
                    const response = await fetch('http://localhost:8000/api/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        },
                        body: JSON.stringify({
                            email: this.email,
                            password: this.password
                        }),
                        credentials: 'include'
                    })
                    const data = await response.json()
                    if (response.ok) {
                        this.success = 'Registration successful! Please log in.'
                        alert('Registration successful! Please log in.')
                        setTimeout(() => {
                            this.$router.push('/login')
                        }, 1000)
                    } else {
                        this.error = data.error || 'Registration failed'
                    }
                }
            } catch (err) {
                this.error = 'An error occurred during registration: ' + err
            }
        }
    }
} 
</script>

<template>
    <el-card class="box-card">
        <h2>{{ $t('register') }}</h2>
        <p v-if="error" class="error">{{error}}</p> 
        <p v-if="success">{{success}}</p>
        <el-form :model="form" ref="registerForm" label-width="120px" @submit.prevent="register">
            <el-form-item :label="$t('enterEmail')" prop="email">
                <el-input v-model="email" id="email" type="email" required :placeholder="$t('enterEmail')"></el-input>
            </el-form-item>
            <el-form-item :label="$t('enterPassword')" prop="password">
                <el-input v-model="password" id="password" type="password" required :placeholder="$t('enterPassword')"></el-input>
            </el-form-item>
            <el-form-item :label="$t('confirmPassword')" prop="password2">
                <el-input v-model="password2" id="password2" type="password" required :placeholder="$t('confirmPassword')"></el-input>
            </el-form-item>
            <br />
            <el-form-item>
                <el-button type="primary" @click="register">{{ $t('submitRegister') }}</el-button>
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