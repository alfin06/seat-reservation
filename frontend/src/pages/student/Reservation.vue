<script>
import { useSettingsStore } from "@/store/setting.js";
import { useAuthStore, getCSRFToken } from "../../store/auth.js";
import { mapState } from 'pinia';

export default {
  name: 'Reservation',
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      rooms: [],
      seats: [],
      reservationForm: {
        room: '',
        seat: '',
        duration: 1,
        date: '',
        time: ''
      },
      selectedRoomSeats: [],
      error: '',
      success: '',
      isLoading: false
    };
  },
  computed:{
    ...mapState(useSettingsStore, ['maxBookingDuration', 'isLoading']),
    effectiveMaxBookingDuration() {
      return this.maxBookingDuration > 0 ? this.maxBookingDuration : 1;
    }
  },
  computed:{
    ...mapState(useSettingsStore, ['maxBookingDuration', 'isLoading']),
    effectiveMaxBookingDuration() {
      return this.maxBookingDuration > 0 ? this.maxBookingDuration : 1;
    }
  },
  watch: {
    'reservationForm.room'(roomId) {
      const selectedRoom = this.rooms.find(r => r.id === roomId);
      this.seats = selectedRoom
        ? selectedRoom.seats.map(seat => ({
            label: seat.name || `Seat ${seat.id}`,
            value: seat.id
          }))
        : [];
      this.selectedRoomSeats = selectedRoom ? selectedRoom.seats : [];
      this.reservationForm.seat = '';
    },
    maxBookingDuration(newMax) {
      const currentMax = newMax > 0 ? newMax : 1;
      if (this.reservationForm.duration > currentMax) {
        this.reservationForm.duration = currentMax;
      }
    }
  },
  async mounted() {
    this.fetchRooms();
    await this.authStore.fetchUser();
    const initialMax = this.maxBookingDuration > 0 ? this.maxBookingDuration : 1;
    if (this.reservationForm.duration > initialMax) {
        this.reservationForm.duration = initialMax;
    } else if (this.reservationForm.duration < 1 ) {
        this.reservationForm.duration = 1;
    }
  },
  methods: {
    selectSeat(seat) {
      if (seat.is_available) {
        this.reservationForm.seat = seat.id;
      }
    },
    async fetchRooms() {
      try {
        const res = await fetch('http://127.0.0.1:8000/dashboard/api/available/');
        const data = await res.json();
        this.rooms = data.rooms || [];
      } catch (err) {
        this.error = 'Failed to fetch rooms ' + err;
      }
    },
    async onSubmit() {
      this.error = '';
      this.success = '';
      this.isLoading = true;
      const token = localStorage.getItem('token');
      // 1. Combine user input into a datetime string
      const localTimeStr = `${this.reservationForm.date}T${this.reservationForm.time}`; // e.g., "2025-05-01T14:00"
      const shanghaiTime = new Date(localTimeStr); // This is in the browser's local time

      // 2. Convert to UTC explicitly
      const utcTimeStr = new Date(
        shanghaiTime.getTime() - (shanghaiTime.getTimezoneOffset() * 60000)
      ).toISOString(); // Will send as UTC

      // 3. Compute reserved_end
      const reservedEnd = new Date(shanghaiTime.getTime() + this.reservationForm.duration * 60 * 60 * 1000);
      const utcReservedEnd = new Date(
        reservedEnd.getTime() - (reservedEnd.getTimezoneOffset() * 60000)
      ).toISOString();

      if (!token) {
        this.error = 'Not authenticated';
        this.isLoading = false;
        return;
      }
      try {
        const res = await fetch('http://127.0.0.1:8000/dashboard/api/reservations/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
          credentials: 'include',
          body: JSON.stringify({
            user_id: this.authStore.user,
            classroom: this.reservationForm.room,
            seat: this.reservationForm.seat,
            duration: this.reservationForm.duration,
            reserved_at: utcTimeStr,
            reserved_end: utcReservedEnd
          })
        });

        const data = await res.json();
        if (res.status === 201) {
          this.isLoading = false;
          this.$router.push({ name: 'booking-success' });
          return;
        } else {
          this.isLoading = false;
          this.$notify({type:"error", text:"Reservation failed! Please try book your seat again in 5 minutes."});
          console.log(data.detail || JSON.stringify(data));
        }
      } catch (err) {
        this.isLoading = false;
        this.$notify({type:"error", text:"Reservation failed! Please try book your seat again in 5 minutes."});
        console.log('Reservation failed ' + err);
      }
    },

    async mounted() {
      await this.authStore.fetchUser();
    },
  }
};
</script>

<template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <main class="col py-4">
        <section class="card shadow-sm">
          <div class="card-body">
            <button class="btn btn-outline-primary mb-3" @click="$router.push('/')">
              <i class="bi bi-arrow-left me-2"></i> {{ $t('backToHome') }}
            </button>

            <h2 class="h5 mb-4 fw-semibold">
              {{ $t('reservationTitle') }}
            </h2>

            <el-form :model="reservationForm" ref="reservationForm" label-width="150px" @submit.prevent="onSubmit">
              <!-- Room -->
              <el-form-item :label="$t('selectStudyRoom')" prop="room">
                <div class="narrow-select">
                  <el-select v-model="reservationForm.room" :placeholder="$t('selectRoomPlaceholder')" style="width: 100%;">
                    <el-option
                      v-for="room in rooms"
                      :key="room.id"
                      :label="room.name"
                      :value="room.id" />
                  </el-select>
                </div>
              </el-form-item>

              <!-- Seat -->
              <el-form-item :label="$t('selectSeat')" prop="seat">
                <div class="narrow-select">
                  <el-select v-model="reservationForm.seat" :placeholder="$t('selectSeatPlaceholder')" style="width: 100%;">
                    <el-option
                      v-for="seat in seats"
                      :key="seat.value"
                      :label="seat.label"
                      :value="seat.value" />
                  </el-select>

                  <!-- Seat Layout Grid (Visible after selecting a room) -->
                  <div v-if="reservationForm.room" class="seat-layout mt-4">
                    <label><i><i class="bi bi-lightning-charge-fill outlet-icon"></i> electricity outlet.</i></label>
                    <h5 class="mb-3">Front Room</h5>
                    <div class="grid-container">
                      <div
                        v-for="seat in selectedRoomSeats"
                        :key="seat.id"
                        class="seat-box"
                        :class="{
                          'selected': seat.id === reservationForm.seat,
                          'unavailable': !seat.is_available,
                          'disabled': !seat.is_disable
                        }"
                        @click="selectSeat(seat)">
                        <div class="seat-content">
                          <span>{{ seat.name || 'Seat ' + seat.id }}</span>
                          <i v-if="seat.has_outlet" class="bi bi-lightning-charge-fill outlet-icon"></i>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-form-item>

              <!-- Date Picker -->
              <el-form-item label="Date" prop="date">
                <el-date-picker
                  v-model="reservationForm.date"
                  type="date"
                  placeholder="Pick a date"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                />
              </el-form-item>

              <!-- Time Picker -->
              <el-form-item label="Time" prop="time">
                <el-time-picker
                  v-model="reservationForm.time"
                  placeholder="Pick a time"
                  format="HH:mm"
                  value-format="HH:mm"
                />
              </el-form-item>

      <!-- Duration -->
      <el-form-item :label="$t('reservationDuration')" prop="duration">
        <el-input-number v-model="reservationForm.duration" :min="1" :max="effectiveMaxBookingDuration" /> 
        &nbsp;&nbsp;<label>{{ $t('hour') }}</label>
      </el-form-item>

              <!-- Submit -->
              <el-form-item>
                <el-button type="primary" @click="onSubmit" :loading="isLoading" :disabled="isLoading">
                  <i class="bi bi-calendar-check me-1"></i>
                  {{ isLoading ? $t('reserving') : $t('reserveSeatButton') }}
                </el-button>
              </el-form-item>

              <!-- Status Messages -->
              <p v-if="success" class="text-success">{{ success }}</p>
              <p v-if="error" class="text-danger">{{ error }}</p>
            </el-form>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.05);
}
.narrow-select {
  width: 25%;
}
@media (max-width: 768px) {
  .narrow-select {
    width: 100%;
  }
}

.seat-layout {
  text-align: center;
}
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 10px;
  justify-items: center;
}
.seat-box {
  padding: 10px;
  width: 60px;
  height: 60px;
  background-color: #e9ecef;
  border: 2px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}
.seat-box:hover {
  background-color: #d6d8db;
}
.seat-box.selected {
  background-color: #007bff;
  color: white;
  border-color: #0056b3;
}
.seat-box.unavailable {
  background-color: #f8d7da;
  color: #721c24;
  cursor: not-allowed;
}
.seat-box.disabled {
  background-color: #dee2e6;
  color: #6c757d;
  text-decoration: line-through;
  cursor: not-allowed;
}
.seat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.outlet-icon {
  font-size: 1rem;
  color: #ffc107; /* Yellow lightning icon */
}
</style>
