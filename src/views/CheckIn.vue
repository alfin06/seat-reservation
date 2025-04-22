<template>
    <el-card class="box-card">
      <h2>{{ $t('checkInTitle') }}</h2>
      <p>{{ $t('checkInDescription') }}</p>
      <el-form
        :model="checkInForm"
        ref="checkInForm"
        label-width="150px"
        @submit.prevent="onCheckIn"
      >
        <el-form-item :label="$t('reservationCodeLabel')" prop="code">
          <el-input v-model="checkInForm.code" :placeholder="$t('reservationCodePlaceholder')" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onCheckIn">{{ $t('checkInButton') }}</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-top: 20px;">
        <el-button type="success" @click="simulateQRScan">{{ $t('simulateQRScanButton') }}</el-button>
      </div>
    </el-card>
  </template>
  
  <script>
  export default {
    name: 'CheckIn',
    data() {
      return {
        checkInForm: {
          code: ''
        }
      }
    },
    methods: {
      onCheckIn() {
        console.log('Check-In Form Submitted:', this.checkInForm)
        // TODO: Connect with your API to process check-in
      },
      simulateQRScan() {
        // Simulate scanning a QR code by autofilling the reservation code.
        this.checkInForm.code = 'QR123456'
        this.onCheckIn()
      }
    }
  }
  </script>
  
  <style scoped>
  .box-card {
    max-width: 500px;
    margin: 20px auto;
    padding: 20px;
  }
  </style>
  