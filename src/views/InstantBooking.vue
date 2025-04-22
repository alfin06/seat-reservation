<template>
  <div class="instant-booking">
    <h2>{{ $t('instantBookingTitle') }}</h2>
    <p>{{ $t('instantBookingDescription') }}</p>
    
    <el-card class="booking-card">
      <div class="header">
        <h3>{{ $t('realTimeAvailability') }}</h3>
        <el-button 
          type="primary" 
          size="small"
          @click="fetchSeats"
          :loading="loading"
        >
          <i class="el-icon-refresh"></i> {{ $t('refreshButton') }}
        </el-button>
      </div>

      <el-table 
        :data="availableSeats" 
        border 
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column 
          prop="room" 
          :label="$t('roomColumnLabel')" 
          width="120" 
        />
        <el-table-column 
          prop="seat" 
          :label="$t('seatColumnLabel')" 
          width="120" 
        />
        <el-table-column 
          :label="$t('statusColumnLabel')" 
          width="120"
        >
          <template #default="{row}">
            <el-tag :type="row.status === 'available' ? 'success' : 'danger'">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="$t('actionColumnLabel')">
          <template #default="{row}">
            <el-button 
              type="primary" 
              size="small" 
              @click="bookSeat(row)"
              :disabled="row.status !== 'available'"
            >
              {{ $t('bookButton') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { ElMessage } from 'element-plus';
import adminApi from '@/services/adminApi';

export default {
  name: 'InstantBooking',
  setup() {
    const { t } = useI18n();
    const availableSeats = ref([]);
    const loading = ref(false);

    const fetchSeats = async () => {
      loading.value = true;
      try {
        const response = await adminApi.getSeatAvailability();
        availableSeats.value = response.data;
      } catch (error) {
        console.error("Error fetching seats:", error);
        // Fallback data matching your original structure
        availableSeats.value = [
          { id: 1, room: 'Room A', seat: 'Seat 1', status: 'available' },
          { id: 2, room: 'Room A', seat: 'Seat 2', status: 'available' },
          { id: 3, room: 'Room B', seat: 'Seat 1', status: 'booked' }
        ];
      } finally {
        loading.value = false;
      }
    };

    const bookSeat = async (seat) => {
      try {
        await adminApi.bookSeat(seat.id);
        ElMessage.success(t('bookingSuccess'));
        await fetchSeats();
      } catch (error) {
        ElMessage.error(t('bookingFailed'));
      }
    };

    // Initial data load
    fetchSeats();

    return {
      availableSeats,
      loading,
      fetchSeats,
      bookSeat,
      t
    };
  }
};
</script>

<style scoped>
.instant-booking {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.booking-card {
  margin-top: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.el-table {
  --el-table-border-color: #ebeef5;
  --el-table-header-bg-color: #f5f7fa;
}

.el-tag--success {
  background: #f0f9eb;
  color: #67c23a;
  border-color: #e1f3d8;
}

.el-tag--danger {
  background: #fef0f0;
  color: #f56c6c;
  border-color: #fde2e2;
}
</style>