<template>
  <el-card class="box-card">
    <h2>{{ $t('instantBookingTitle') }}</h2>
    <p>{{ $t('instantBookingDescription') }}</p>
    <el-table :data="availableSeats" style="width: 100%;">
      <el-table-column prop="room" :label="$t('roomColumnLabel')" width="120" />
      <el-table-column prop="seat" :label="$t('seatColumnLabel')" width="120" />
      <el-table-column :label="$t('actionColumnLabel')">
        <template #default="scope">
          <el-button type="primary" size="small" @click="bookSeat(scope.row)">
            {{ $t('bookButton') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script>
export default {
  name: 'InstantBooking',
  data() {
    return {
      availableSeats: [
        { id: 1, room: 'Room A', seat: 'Seat 1' },
        { id: 2, room: 'Room A', seat: 'Seat 2' },
        { id: 3, room: 'Room B', seat: 'Seat 1' }
      ]
    }
  },
  methods: {
    bookSeat(seat) {
      console.log('Instant booking seat:', seat)
      // TODO: Hook this into your API for real-time booking
    }
  }
}
</script>

<style scoped>
.box-card {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
}
</style>
