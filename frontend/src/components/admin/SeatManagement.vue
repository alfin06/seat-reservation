<template>
  <div class="seat-management">
    <div class="action-bar">
      <el-select
        v-model="selectedRoomId"
        placeholder="Select a room"
        clearable
        style="width: 300px;">
        <el-option
          v-for="room in rooms"
          :key="room.id"
          :label="room.name"
          :value="room.id" />
      </el-select>

      <el-input
        v-model="searchQuery"
        placeholder="Search seat..."
        clearable
        style="width: 300px; margin-left: 10px;"
        :disabled="!selectedRoomId" />
    </div>

    <el-dialog
      title="Edit Seat"
      v-model="editDialogVisible"
      width="500px">
      <el-form :model="editForm" label-width="120px">
        <!-- <el-form-item label="Location">
          <el-input v-model="editForm.location" />
        </el-form-item>

        <el-form-item label="Classroom">
          <el-input v-model="editForm.classroom" />
        </el-form-item> -->

        <el-form-item label="Has Outlet">
          <el-switch v-model="editForm.has_outlet" />
        </el-form-item>

        <el-form-item label="Available">
          <el-switch v-model="editForm.is_available" />
        </el-form-item>

        <el-form-item label="Disabled">
          <el-switch v-model="editForm.is_disable" />
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitEdit">Save</el-button>
      </div>
    </el-dialog>

    <template v-if="selectedRoomSeats.length">
      <el-table :data="displayedSeats" border>
        <el-table-column prop="name" label="Seat Name" sortable />
        <el-table-column prop="location" label="Location" />
        <el-table-column prop="classroom" label="Classroom" width="90" />

        <el-table-column label="Outlet" width="90">
          <template #default="{ row }">
            <el-tag :type="row.has_outlet.value ? 'success' : 'info'">
              {{ row.has_outlet.display }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Available" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_available.value ? 'success' : 'warning'">
              {{ row.is_available.display }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_disable.value ? 'danger' : 'info'">
              {{ row.is_disable.display }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Last Updated" width="180">
          <template #default="{ row }">
            {{ formatDate(row.updated_at) }}
          </template>
        </el-table-column>

        <el-table-column label="Actions" width="150">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" size="mini" @click="openEditModal(row)">
                <i class="bi bi-pencil"></i>&nbsp;Edit
              </el-button>
              <el-button type="warning" size="mini" @click="toggleEnable(row)">
                <i class="bi bi-eye"></i>&nbsp;Enable
              </el-button>
              <el-button type="danger" size="mini" @click="toggleDisable(row)">
                <i class="bi bi-x"></i>&nbsp;Disable
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>

        <el-table-column label="QR Code" width="100">
          <template #default="{ row }">
            <el-button
              size="mini"
              @click="generateQR(row)"
              class="open-btn">
              <i class="bi bi-qr-code"></i>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          background
          layout="prev, pager, next"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="filteredSeats.length"
          @current-change="handlePageChange" />
      </div>
    </template>

    <!-- QR Modal -->
    <div v-if="showQR" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <qrcode-vue ref="qrCanvas" :value="qrValue" :size="size" level="H" render-as="svg" />
        <div class="qr-text">ID: {{ qrValue }}</div>
        <div class="button-group">
          <el-button size="mini" @click="downloadQR">Download</el-button>
          <el-button size="mini" @click="closeModal">Close</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import QrcodeVue from 'qrcode.vue';
import dayjs from 'dayjs';

export default {
  components: { QrcodeVue },
  data() {
    return {
      rooms: [],
      selectedRoomId: null,
      currentPage: 1,
      pageSize: 15,
      searchQuery: '',
      showQR: false,
      qrValue: '',
      size: 200,
      editDialogVisible: false,
      editForm: {
        id: null,
        location: '',
        classroom: '',
        has_outlet: false,
        is_available: true,
        is_disable: false
      }
    };
  },
  computed: {
    selectedRoomSeats() {
      const room = this.rooms.find(r => r.id === this.selectedRoomId);
      return room ? room.seats.map(seat => ({
        ...seat,
        name: `Seat ${seat.id}`,
        location: seat.location,
        classroom: seat.classroom,
        is_available: {
          value: seat.is_available,
          display: seat.is_available ? 'Available' : 'Unavailable'
        },
        is_disable: {
          value: seat.is_disable,
          display: seat.is_disable ? 'Disabled' : 'Active'
        },
        has_outlet: {
          value: seat.has_outlet,
          display: seat.has_outlet ? 'Yes' : 'No'
        },
        updated_at: seat.update_at
      })) : [];
    },
    filteredSeats() {
      return this.selectedRoomSeats.filter(seat =>
        seat.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    displayedSeats() {
      const start = (this.currentPage - 1) * this.pageSize;
      return this.filteredSeats.slice(start, start + this.pageSize);
    }
  },
  methods: {
    openEditModal(row) {
      console.log('Opening edit modal for:', row);
      this.editForm = {
        id: row.id,
        location: row.location,
        classroom: row.classroom,
        has_outlet: row.has_outlet.value == 1 ? true : false,
        is_available: row.is_available.value == 1 ? true : false,
        is_disable: row.is_disable.value == 1 ? true : false
      };
      this.editDialogVisible = true;
    },
    async submitEdit() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/seats/update/',
          this.editForm,
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );

        if (res.data.message?.includes('successfully')) {
          this.$message.success(res.data.message);
          this.editDialogVisible = false;
          await this.fetchRoomsAndSeats();
        } else {
          this.$message.error(res.data.message || 'Update failed.');
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error updating seat.');
      }
    },
    async fetchRoomsAndSeats() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://127.0.0.1:8000/dashboard/api/allseats/', {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (res.data.rooms) {
          this.rooms = res.data.rooms.map(r => ({
            ...r,
            name: r.name || `Room ${r.id} - ${r.location}`,
            seats: r.seats || []
          }));
        } else {
          this.$message.error('No rooms found');
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error fetching rooms and seats');
      }
    },
    handlePageChange(newPage) {
      this.currentPage = newPage;
    },
    async toggleEnable(row) {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/seats/enable/',
          { id: row.id },
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        if (res.data.message?.includes('successfully')) {
          this.$message.success(res.data.message);
          await this.fetchRoomsAndSeats();
        } else {
          this.$message.error(res.data.message || 'Failed to enable seat.');
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling seat.');
      }
    },
    async toggleDisable(row) {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/seats/disable/',
          { id: row.id },
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        if (res.data.message?.includes('successfully')) {
          this.$message.success(res.data.message);
          await this.fetchRoomsAndSeats();
        } else {
          this.$message.error(res.data.message || 'Failed to disable seat.');
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling seat.');
      }
    },
    generateQR(row) {
      this.qrValue = row.id.toString();
      this.showQR = true;
    },
    downloadQR() {
      const svg = this.$refs.qrCanvas.$el;
      const svgData = new XMLSerializer().serializeToString(svg);
      const canvas = document.createElement('canvas');
      canvas.width = this.size;
      canvas.height = this.size;
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.onload = () => {
        ctx.drawImage(img, 0, 0);
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = `qr_${this.qrValue}.png`;
        link.click();
      };
      img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    },
    closeModal() {
      this.showQR = false;
    },
    formatDate(dateString) {
      return dayjs(dateString).format('YYYY-MM-DD HH:mm:ss')
    }
  },
  mounted() {
    this.fetchRoomsAndSeats();
  }
};
</script>

<style scoped>
.action-bar {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: calc(var(--qr-size) + 40px);
}
.modal-content {
  --qr-size: 200px;
}
.open-btn {
  padding: 0.3rem 0.6rem;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.qr-text {
  margin-top: 10px;
  font-weight: bold;
  text-align: center;
}
.button-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.modal-content svg {
  width: var(--qr-size);
  height: var(--qr-size);
}
.dialog-footer {
  text-align: right;
}
</style>
