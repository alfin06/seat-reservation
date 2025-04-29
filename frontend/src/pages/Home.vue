<script>
import {useAuthStore} from '../store/auth.js'
import {useRouter} from 'vue-router'

export default {
    setup() {
        const authStore = useAuthStore()
        const router = useRouter()

        return {
            authStore,
            router
        }
    },
    methods: {
        async logout() {
            try {
                await this.authStore.logout(this.$router)
            } catch (error) {
                console.error(error)
            }
        }
    },
    async mounted() {
        await this.authStore.fetchUser()
    }
} 
</script>

<template>
    <div class="home-container">
        <h1 class="welcome-title">Study Seat Reservation System</h1>
        
        <div class="system-description">
            <p>Welcome to our smart study space management system. Here you can:</p>
            <ul>
                <li>Reserve study seats in advance</li>
                <li>Find available quiet spaces to study</li>
                <li>Manage your bookings</li>
                <li>Get notifications about your reservations</li>
            </ul>
        </div>

        <div v-if="authStore.isAuthenticated" class="user-info">
            <h2>Welcome, {{ authStore.user?.name || authStore.user?.username }}!</h2>
            
            <div class="user-details">
                <p><strong>Email:</strong> {{ authStore.user?.email }}</p>
                <p><strong>Role:</strong> {{ authStore.user?.role || 'Student' }}</p>
                <p><strong>Account Status:</strong> Active</p>
                <p><strong>Last Login:</strong> {{ new Date(authStore.user?.last_login).toLocaleString() }}</p>
            </div>
            <div class="actions"> 
                <button 
                    @click="$router.push(authStore.user?.role === 'ADMIN' ? '/admin-dashboard' : '/reservation')"  
                    class="btn primary"
                >
                    {{ authStore.user?.role === 'ADMIN' ? 'Admin Dashboard' : 'Reserve a Seat' }}
                </button>
                <button @click="logout" class="btn secondary">Logout</button>
            </div>
        </div>
        
        <div v-else class="auth-prompt">
            <p>Please <router-link to="/login">login</router-link> or <router-link to="/register">register</router-link> to make a seat reservation.</p>
        </div>
    </div>
</template>

<style scoped>
.home-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

.welcome-title {
    color: #2c3e50;
    text-align: center;
    margin-bottom: 2rem;
}

.system-description {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
    color: #495057;
}

.system-description ul {
    list-style-type: none;
    padding: 0;
    margin: 1rem 0;
}

.system-description li {
    padding: 0.5rem 0;
    padding-left: 1.5rem;
    position: relative;
}

.system-description li:before {
    content: "✓";
    color: #3498db;
    position: absolute;
    left: 0;
}

.user-info {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 2rem;
    margin-top: 2rem;
}

.user-details {
    margin: 1.5rem 0;
}

.user-details p {
    margin: 0.5rem 0;
    color: #495057;
}

.actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn.primary {
    background: #3498db;
    color: white;
}

.btn.primary:hover {
    background: #2980b9;
}

.btn.secondary {
    background: #e74c3c;
    color: white;
}

.btn.secondary:hover {
    background: #c0392b;
}

.auth-prompt {
    text-align: center;
    margin-top: 2rem;
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.auth-prompt a {
    color: #3498db;
    text-decoration: none;
    font-weight: 600;
}

.auth-prompt a:hover {
    text-decoration: underline;
}
</style>