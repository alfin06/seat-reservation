<template>
    <div class="container my-5">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <el-card class="box-card card-body" v-loading="loading" element-loading-text="Please wait..." element-loading-spinner="el-icon-loading">
                    <h2>Create a new Password</h2>
                    <p v-if="error" class="error text-danger">{{error}}</p> 
                    <p v-if="success" class="success text-success">{{success}}</p>
                    <br/>
                    <el-form :model="form" ref="resetForm" label-width="120px" @submit.prevent="resetPassword" class="form-horizontal form-material">
                        <el-form-item :label="$t('enterPassword')" prop="password" class="form-label">
                            <el-input v-model="password" id="password" type="password" required :placeholder="$t('enterPassword')"></el-input>
                        </el-form-item>
                        <el-form-item :label="$t('confirmPassword')" prop="password2" class="form-label">
                            <el-input v-model="password2" id="password2" type="password" required :placeholder="$t('confirmPassword')"></el-input>
                        </el-form-item>
                        <br/><br/>
                        <el-button type="primary" @click="resetPassword">Submit</el-button>
                    </el-form>
                    <div class="links-container">
                        <p>Remember your password? <el-link type="primary" @click="onLogin">Login</el-link></p>
                        <p>Don't have an account? <el-link type="primary" @click="onRegister">Register</el-link></p>
                    </div>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import {getCSRFToken} from '../../store/auth'

export default {
    name: 'ResetPassword',
    data() {
        return {
            token: '',
            password: '',
            password2: '',
            loading: false,
            success: false,
        }
    },
    mounted() {
        this.token = this.$route.params.token;
    },
    methods: {
        async resetPassword() {
            try {
                this.loading = true; // Show loader
                if (this.password != this.password2) {
                    this.error = "Passwords do not match!"
                    return
                }

                const response = await fetch('http://localhost:8000/users/auth/password-reset-confirm/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        token: this.token,
                        password: this.password,
                        confirm_password: this.password2
                    }),
                    credentials: 'include'
                })

                if (!response.ok) {
                    this.$notify({
                        type: "error",
                        text: "Something wrong! Please wait for 5 minute and reset your password again."
                    })
                }
                else {
                    //this.success = 'Password reset instructions have been sent to your email.'
                    this.$notify({
                        type: "success",
                        text: "Password has been changed! You can login now."
                    })
                    setTimeout(() => {
                        this.$router.push('/login');
                    }, 1000);
                }
                
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