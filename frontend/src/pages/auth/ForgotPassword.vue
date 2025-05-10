<script>
import { useAuthStore } from '../../store/auth'
import logo from '@/assets/app_logo.png';

export default {
    name: 'ForgotPassword',
    data() {
        return {
            email: '',
            error: '',
            success: '',
            logo,
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
    <div class="container justify-content-center align-items-center forgot">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="box-card card-body text-center" v-loading="loading" element-loading-text="Please wait..." element-loading-spinner="el-icon-loading">
                    <div class="text-center mb-4">
                      <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 150px;" />
                    </div>
                    <p class="description">{{ $t('forgotInstruction') }}</p>
                    <p v-if="error" class="error text-danger">{{error}}</p> 
                    <p v-if="success" class="success text-success">{{success}}</p>
                    <el-form :model="form" ref="resetForm" label-width="120px" @submit.prevent="resetPassword" class="form-horizontal form-material">
                        <el-input v-model="email" id="email" type="email" required :placeholder="$t('enterEmail')"></el-input>
                        <br/><br/>
                        <el-button type="primary" @click="resetPassword">{{ $t('sendInstructions') }}</el-button>
                    </el-form>
                    <br/>
                    <div class="links-container">
                        <p>{{ $t('rememberPwd') }}? <el-link type="primary" @click="onLogin">{{ $t('login') }}</el-link></p>
                    </div>
                  </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.box-card {
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  background: #fff;
}

.description {
  color: #606266;
  margin: 1rem 0;
  text-align: center;
  font-weight: bold;
}

.error {
  color: #f56c6c;
  margin-bottom: 1rem;
}

.success {
  color: #67c23a;
  margin-bottom: 1rem;
}

.form-item {
  margin-bottom: 1.5rem;
}

.input-field {
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
}

.input-field:focus {
  border-color: #409eff;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.3);
}

.el-form-item__label {
  font-weight: 600;
  margin-bottom: 8px;
}

.el-button {
  padding: 10px 0;
  border-radius: 8px;
}

.links-container p {
  margin: 0.5rem 0;
}

:deep(.el-link) {
  font-weight: 600;
  margin-left: 4px;
}

:deep(.el-button) {
  min-width: 200px;
}

.el-input {
  width: 100%;
}

.forgot {
  margin-top:10%;
  padding: 15px;
}

</style>