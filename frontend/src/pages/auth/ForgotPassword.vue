<script>
import { useAuthStore } from '../../store/auth'

export default {
    name: 'ForgotPassword',
    data() {
        return {
            email: '',
            error: '',
            success: '',
            loading: false, // Loader state
        }
    },
    methods: {
        async resetPassword() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
            try {
                this.loading = true; // Show loader
                if(!emailRegex.test(this.email)) {
                    this.error = "Invalid email address!"
                    return
                }

                const authStore = useAuthStore()
                await authStore.resetPassword(this.email)

                //this.success = 'Password reset instructions have been sent to your email.'
                this.$notify({
                    type: "success",
                    text: "Password reset instructions have been sent to your email."
                })
            } catch (error) {
                //this.error = error.message || 'Failed to send reset instructions'
                this.$notify({
                    type: "error",
                    text: this.error
                })
            } finally {
                this.loading = false; // Hide loader
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

<template>
    <div class="container my-5">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <el-card class="box-card card-body" v-loading="loading" element-loading-text="Please wait..." element-loading-spinner="el-icon-loading">
                    <h2>Reset Password</h2>
                    <p class="description">Enter your email address and we'll send you instructions to reset your password.</p>
                    <p v-if="error" class="error text-danger">{{error}}</p> 
                    <p v-if="success" class="success text-success">{{success}}</p>
                    <el-form :model="form" ref="resetForm" label-width="120px" @submit.prevent="resetPassword" class="form-horizontal form-material">
                        <el-input v-model="email" id="email" type="email" required :placeholder="$t('enterEmail')"></el-input>
                        <br/><br/>
                        <el-button type="primary" @click="resetPassword">{{ $t('sendInstructions') }}</el-button>
                    </el-form>
                    <div class="links-container">
                        <p>Remember your password? <el-link type="primary" @click="onLogin">{{ $t('login') }}</el-link></p>
                        <p>Don't have an account? <el-link type="primary" @click="onRegister">{{ $t('register') }}</el-link></p>
                    </div>
                </el-card>
            </div>
        </div>
    </div>
</template>

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

#email {
    text-align: center;
}
</style> 