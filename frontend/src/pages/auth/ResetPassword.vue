<script>
import {getCSRFToken} from '../../store/auth';
import logo from '@/assets/app_logo.png';

export default {
    name: 'ResetPassword',
    data() {
        return {
            token: '',
            password: '',
            password2: '',
            logo,
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
                        title: "ERROR",
                        duration: 5000,
                        type: "error",
                        text: "Something wrong! Please wait for 5 minute and reset your password again."
                    })
                }
                else {
                    //this.success = 'Password reset instructions have been sent to your email.'
                    this.$notify({
                        title: "SUCCESS",
                        duration: 5000,
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
                    title: "ERROR",
                    type: "error",
                    duration: 5000,
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
    <div class="container justify-content-center align-items-center forgot">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <el-card class="box-card card-body" v-loading="loading" element-loading-text="Please wait..." element-loading-spinner="el-icon-loading">
                    <div class="text-center mb-4">
                      <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 150px;" />
                    </div>
                    <p class="description">{{ $t('forgotInstruction2') }}</p>

                    <el-form :model="form" ref="resetForm" @submit.prevent="resetPassword" label-position="top" class="p-3">
                        <el-form-item :label="$t('enterPassword')">
                            <el-input
                            v-model="password"
                            type="password"
                            required
                            :placeholder="$t('enterPassword')"
                            show-password
                            clearable
                            class="underline-input" />
                        </el-form-item>

                        <el-form-item :label="$t('confirmPassword')">
                            <el-input
                            v-model="password2"
                            type="password"
                            required
                            :placeholder="$t('confirmPassword')"
                            show-password
                            clearable
                            class="underline-input" />
                        </el-form-item>
                        <br/>
                        <el-form-item class="mb-0">
                            <el-button type="primary" @click="resetPassword" class="w-100">
                            {{ $t('submit') }}
                            </el-button>
                        </el-form-item>
                    </el-form>
                    <div class="links-container">
                        <p>Remember your password? <el-link type="primary" @click="onLogin">Login</el-link></p>
                        <!-- <p>Don't have an account? <el-link type="primary" @click="onRegister">Register</el-link></p> -->
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
  font-weight: bold;
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

:deep(.el-form-item__label) {
  font-weight: bold;
}

.forgot {
  padding: 15px;
}
</style> 