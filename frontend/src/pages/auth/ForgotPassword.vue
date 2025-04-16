<template>
    <el-card class="box-card card-body">
        <h2>Reset Password</h2>
        <p class="description">Enter your email address and we'll send you instructions to reset your password.</p>
        <p v-if="error" class="error text-danger">{{error}}</p> 
        <p v-if="success" class="success text-success">{{success}}</p>
        <el-form :model="form" ref="resetForm" label-width="120px" @submit.prevent="resetPassword" class="form-horizontal form-material">
            <el-form-item label="Email" prop="email" class="form-label">
                <el-input v-model="email" id="email" type="email" required placeholder="Enter your email">
                </el-input>
            </el-form-item>
            <el-form-item class="form-spacing">
                <el-button type="primary" @click="resetPassword">Send Reset Instructions</el-button>
            </el-form-item>
        </el-form>
        <div class="links-container">
            <p>Remember your password? <el-link type="primary" @click="onLogin">Login</el-link></p>
            <p>Don't have an account? <el-link type="primary" @click="onRegister">Register</el-link></p>
        </div>
    </el-card>
</template>

<script>
import { useAuthStore } from '../../store/auth'

export default {
    name: 'ForgotPassword',
    data() {
        return {
            email: '',
            error: '',
            success: ''
        }
    },
    methods: {
        async resetPassword() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
            try {
                if(!emailRegex.test(this.email)) {
                    this.error = "Invalid email address!"
                    return
                }

                const authStore = useAuthStore()
                await authStore.resetPassword(this.email)

                this.success = 'Password reset instructions have been sent to your email.'
                this.$notify({
                    type: "success",
                    text: "Password reset instructions have been sent to your email."
                })
            } catch (error) {
                this.error = error.message || 'Failed to send reset instructions'
                this.$notify({
                    type: "error",
                    text: this.error
                })
            }
        },
        onLogin() {
            this.$router.push('/login')
        },
        onRegister() {
            this.$router.push('/register')
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

.description {
    color: #606266;
    margin: 1rem 0;
    text-align: center;
}

.error {
    color: #f56c6c;
    margin-bottom: 1rem;
}

.success {
    color: #67c23a;
    margin-bottom: 1rem;
}

.form-spacing {
    margin-top: 1.5rem;
    text-align: center;
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

:deep(.el-button) {
    min-width: 200px;
}
</style> 