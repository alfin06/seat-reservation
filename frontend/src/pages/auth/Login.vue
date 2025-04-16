<script>
import {useAuthStore} from '../../store/auth';

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
            role: "STUDENT", // Default role
            error: "",
            roles: [
                { label: 'Student', value: 'STUDENT' },
                { label: 'Admin', value: 'ADMIN' }
            ]
        }
    },
    methods: {
        async login() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if(!emailRegex.test(this.email)) {
                this.error = "Invalid email address!"
                return
            }

            try {
                await this.authStore.login({
                    email: this.email,
                    password: this.password
                }, this.$router)
            } catch (error) {
                this.error = "Login failed: Please check your credentials!"
            }
        },
        resetError() {
            this.error = ""
        },
        onRegister() {
            this.$router.push('/register')
        },
        onForgotPassword() {
            this.$router.push('/forgot-password')
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
        <p v-if="error" class="error text-danger">{{ error }}</p>
        <el-form :model="form" ref="loginForm" label-width="120px" @submit.prevent="login" class="form-horizontal form-material">
            <el-form-item :label="$t('enterEmail')" prop="email" class="form-label">
                <el-input v-model="email" id="email" type="text" required @input="resetError" :placeholder="$t('enterEmail')"></el-input>
            </el-form-item>
            <el-form-item :label="$t('enterPassword')" prop="password" class="form-label">
                <el-input v-model="password" id="password" type="password" required @input="resetError" :placeholder="$t('enterPassword')"></el-input>
            </el-form-item>
            <!-- <el-form-item label="Role" prop="role" class="form-label">
                <el-select v-model="role" placeholder="Select role">
                    <el-option
                        v-for="option in roles"
                        :key="option.value"
                        :label="option.label"
                        :value="option.value"
                    ></el-option>
                </el-select>
            </el-form-item> -->
            <br/>
            <el-button type="primary" @click="login">{{ $t('submitLogin') }}</el-button>
            
        </el-form>
        <div class="links">
            <p><el-link @click="onForgotPassword">{{ $t('forgetPassword') }}?</el-link></p>
            <p>{{ $t('noAccount') }}? <el-link @click="onRegister">{{ $t('register') }}</el-link></p>
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

.links {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

:deep(.el-select) {
    width: 100%;
}
</style>