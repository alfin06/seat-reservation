<script>
  export default {
    name: "VerifyEmail",
    data() {
      return {
        loading: true,
        success: false,
      };
    },
    mounted() {
      const token = this.$route.params.token;
      fetch(`http://localhost:8000/users/auth/verify-email/${token}`, {
        method: "GET",
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error("Verification failed");
          }
          return res.json();
        })
        .then(() => {
          this.success = true;
        })
        .catch(() => {
          this.success = false;
        })
        .finally(() => {
          this.loading = false;
          setTimeout(() => {
            this.$router.push({ name: "login" });
          }, 5000);
        });
    },
  };
</script>

<template>
    <div class="verify-email">
      <div v-if="loading">Verifying your email...</div>
      <div v-else>
        <div v-if="success" class="success-message">
          ✅ Your email has been successfully verified! Please wait 5 seconds ...
        </div>
        <div v-else class="error-message">
          ❌ Verification failed. The token may be invalid or expired.
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .verify-email {
    text-align: center;
    margin-top: 50px;
    font-size: 18px;
  }
  .success-message {
    color: green;
  }
  .error-message {
    color: red;
  }
  </style>
  