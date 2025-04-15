<script>
import {getCSRFToken} from '../store/auth'

export default {
    data() {
        return {
            email: '',
            password: '',
            password2: '',
            error: '',
            success: '',
            role: 'STUDENT',
            roles: [
                {
                    value: 'STUDENT',
                    label: 'Student'
                },
                {
                    value: 'ADMIN',
                    label: 'Admin'
                }
            ]
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
                    const response = await fetch('http://localhost:8000/users/auth/register/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        },
                        body: JSON.stringify({
                            email: this.email,
                            name: this.email,
                            password: this.password,
                            confirm_password: this.password2,
                            role: this.role
                        }),
                        credentials: 'include'
                    })
                    
                    if (!response.ok) {
                        const contentType = response.headers.get("content-type");
                        if (contentType && contentType.indexOf("application/json") !== -1) {
                            const data = await response.json();
                            this.error = data.error || 'Registration failed';
                        } else {
                            this.error = `Registration failed: ${response.status} ${response.statusText}`;
                        }
                        return;
                    }

                    const data = await response.json();
                    this.success = 'Registration successful! Please log in.';
                    this.$notify({type:"success", text:"Registration successful! Please log in."});
                    setTimeout(() => {
                        this.$router.push('/login');
                    }, 1000);
                }
            } catch (err) {
                this.error = 'An error occurred during registration: ' + err
            }
        },
        onLogin() {
            // For example, redirect to the login page.
            this.$router.push('/login');
        },
        onForgotPassword() {
            this.$router.push('/forgot-password');
        }
    }
} 
</script>

<template>
    <el-card class="box-card card-body">
        <h2>{{ $t('register') }}</h2>
        <p v-if="error" class="error text-danger">{{error}}</p> 
        <p v-if="success" class="success text-success">{{success}}</p>
        <el-form :model="form" ref="registerForm" label-width="120px" @submit.prevent="register" class="form-horizontal form-material">
            <el-form-item :label="$t('enterEmail')" prop="email" class="form-label">
                <el-input v-model="email" id="email" type="email" required :placeholder="$t('enterEmail')"></el-input>
            </el-form-item>
            <el-form-item :label="$t('enterPassword')" prop="password" class="form-label">
                <el-input v-model="password" id="password" type="password" required :placeholder="$t('enterPassword')"></el-input>
            </el-form-item>
            <el-form-item :label="$t('confirmPassword')" prop="password2" class="form-label">
                <el-input v-model="password2" id="password2" type="password" required :placeholder="$t('confirmPassword')"></el-input>
            </el-form-item>
            <el-form-item label="Role" prop="role" class="form-label form-spacing">
                <el-select v-model="role" placeholder="Select role">
                    <el-option
                        v-for="role in roles"
                        :key="role.value"
                        :label="role.label"
                        :value="role.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item class="form-spacing">
                <el-button type="primary" @click="register">{{ $t('submitRegister') }}</el-button>
            </el-form-item>
        </el-form>
        <div class="links-container">
            <p>Already have an account? <el-link type="primary" @click="onLogin">{{ $t('login') }}</el-link></p>
            <p>Forgot your password? <el-link type="primary" @click="onForgotPassword">Reset Password</el-link></p>
        </div>
    </el-card>
</template>

<style scoped>
.box-card {
    max-width: 500px;
    margin: 50px auto;
    padding: 20px;
}

.error {
    color: #f56c6c;
    margin-bottom: 1rem;
}

.success {
    color: #67c23a;
    margin-bottom: 1rem;
}

.el-select {
    width: 100%;
}

.form-spacing {
    margin-top: 1.5rem;
}

:deep(.el-form-item) {
    margin-bottom: 1.5rem;
}

.links-container {
    margin-top: 1.5rem;
    text-align: center;
}

.links-container p {
    margin: 0.5rem 0;
}

:deep(.el-link) {
    font-weight: 600;
    margin-left: 0.25rem;
}
</style>