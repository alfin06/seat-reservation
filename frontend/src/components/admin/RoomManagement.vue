<template>
  <div class="room-management">
    <div class="action-bar">
      <el-button type="primary" @click="showAddRoomForm">
        <i class="bi-plus"></i> Add Classroom
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="Search room..."
        clearable
        style="width: 300px; margin-left: 10px;" />
    </div>

    <!-- Add Room Popup Form Dialog -->
    <div v-if="addRoomDialogVisible" class="custom-modal-overlay addRoom" @click.self="addRoomDialogVisible = false">
      <div class="custom-modal">
        <div class="modal-header">
          <h3>{{ dialogMode === 'edit' ? 'Edit Room' : 'Add New Room' }}</h3>
        </div>
        
        <div class="modal-body">
          <el-form
            :model="newRoom"
            :rules="roomRules"
            ref="roomForm"
            label-position="top">

            <el-form-item label="Classroom Name" prop="classroom">
              <el-input
                v-model="newRoom.name"
                placeholder="e.g., Room 123"
                clearable />
            </el-form-item>

            <el-form-item label="Location" prop="location">
              <el-input
                v-model="newRoom.location"
                placeholder="e.g., Building 2, Floor 3"
                clearable />
            </el-form-item>
            
            <el-form-item label="Capacity" prop="capacity">
              <el-input-number
                v-model="newRoom.capacity"
                :min="1"
                :max="1000"
                controls-position="right"
                style="width: 100%" />
            </el-form-item>
          </el-form>
        </div>

        <div class="modal-footer">
          <el-button @click="handleCancel">Cancel</el-button>
          <el-button type="primary" @click="submitRoomForm" :loading="isSubmitting">
            Submit
          </el-button>
        </div>
      </div>
      <hr/>
    </div>
    <br/>

    <el-table :data="displayedRooms" border>
      <!-- Name -->
      <el-table-column prop="name" label="Classroom" sortable />
      <!-- Location -->
      <el-table-column prop="location" label="Location" sortable />
      <el-table-column prop="number_of_seat" label="Number of Seat" width="150"/>
      <!-- Availability -->
      <el-table-column label="Available" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_available.value ? 'success' : 'warning'">
            {{ row.is_available.display }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- Disabled -->
      <el-table-column label="Status" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_disable.value ? 'danger' : 'info'">
            {{ row.is_disable.display }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- Updated At -->
      <el-table-column prop="updated_at" label="Last Updated" width="180" />

      <!-- Actions -->
      <el-table-column label="Actions" width="320">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              type="primary"
              size="mini"
              @click="editRoom(row)">
              <i class="bi bi-pencil"></i>&nbsp;Edit
            </el-button>
            <el-button
              type="warning"
              size="mini"
              @click="toggleEnable(row)">
              <i class="bi bi-eye"></i>&nbsp;Enable
            </el-button>
            <el-button
              type="danger"
              size="mini"
              @click="toggleDisable(row)">
              <i class="bi bi-x"></i>&nbsp;Disable
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- QR Modal (single instance) -->
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

    <!-- Pagination Controls -->
    <div class="pagination">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="filteredRooms.length"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import QrcodeVue from 'qrcode.vue'

export default {
  components: {
    QrcodeVue
  },
  data() {
    return {
      newRoom: {
        name: '',
        location: '',
        capacity: null,
      },
      roomRules: {
        name: [
          { required: true, message: 'Please enter room name', trigger: 'blur' }
        ],
        location: [
          { required: true, message: 'Please enter room location', trigger: 'blur' }
        ],
        capacity: [
          { required: true, message: 'Please enter room capacity', trigger: 'blur' },
          { type: 'number', min: 1, message: 'Capacity must be at least 1', trigger: 'blur' }
        ]
      },

      addRoomDialogVisible: false,
      isSubmitting: false,
      currentPage: 1,
      pageSize: 15,
      rooms: [],          // fetched from API
      searchQuery: '',
      dialogVisible: false,
      dialogMode: 'add',
      currentRoom: this.getDefaultRoom(),
      showQR: false,
      qrValue: '',
      size: 200           // QR code pixel size
    }
  },
  computed: {
    filteredRooms() {
      return this.rooms.filter(r =>
        r.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    displayedRooms() {
        const start = (this.currentPage - 1) * this.pageSize
        const end = start + this.pageSize
        return this.filteredRooms.slice(start, end)
    },
    dialogTitle() {
      return this.dialogMode === 'add' ? 'Add New Room' : 'Edit Room'
    }
  },
  methods: {
    showAddRoomForm() {
      //this.addRoomDialogVisible = true
      this.dialogMode = 'add'; // Always start fresh
      this.resetRoomForm();    // Clear any old data
      this.addRoomDialogVisible = true;
    },

    resetRoomForm() {
      this.newRoom = {
        name: '',
        location: '',
        capacity: null,
      }
      this.$refs.roomForm?.resetFields()
    },

    editRoom(room) {
      this.dialogMode = 'edit';
      this.currentRoom = { ...room }; // Clone the object
      this.newRoom = {
        name: room.name,
        location: room.location,
        capacity: room.number_of_seat
      };
      this.addRoomDialogVisible = true;
    },

    handleCancel() {
      this.addRoomDialogVisible = false;
      this.dialogMode = 'add'; // Reset to default mode
      this.resetRoomForm();    // Clear form data
    },

    async submitRoomForm() {
      try {
        await this.$refs.roomForm.validate();
        const token = localStorage.getItem('token');
        this.isSubmitting = true;

        const payload = {
          name: this.newRoom.name,
          location: this.newRoom.location,
          number_of_seats: Number(this.newRoom.capacity)
        };

        let response;
        if (this.dialogMode === 'edit') {
          payload.id = this.currentRoom.id;
          response = await axios.put(
            'http://127.0.0.1:8000/dashboard/admin/classroom/update/',
            payload,
            {
              headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
              }
            }
          );
        } else {
          response = await axios.post(
            'http://127.0.0.1:8000/dashboard/admin/classroom/insert/',
            payload,
            {
              headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
              }
            }
          );
        }

        if ([200, 201].includes(response.status)) {
          this.$message.success(`Room ${this.dialogMode === 'edit' ? 'updated' : 'created'} successfully!`);
          this.addRoomDialogVisible = false;
          await this.fetchRooms();
          this.$emit('room-status-changed');
          this.resetRoomForm();
        } else {
          this.$message.error(response.data.message || 'Unexpected response');
        }
      } catch (err) {
        if (err.name === 'ValidationError') return;
        let msg = this.dialogMode === 'edit' ? 'Failed to update room' : 'Failed to create room';
        if (err.response) {
          msg = err.response.data.message || err.response.data.error || `Server error: ${err.response.status}`;
        }
        this.$message.error(msg);
      } finally {
        this.isSubmitting = false;
      }
    },

    handlePageChange(newPage) {
        this.currentPage = newPage
    },

    getDefaultRoom() {
      return {
        id: null,
        name: '',
        location: '',
        number_of_seat: 0,
        is_available: { value: 1, display: 'Available' },
        is_disable:   { value: 0, display: 'Active' },
        updated_at: ''
      }
    },

    async fetchRooms() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(
          'http://127.0.0.1:8000/dashboard/admin/classroom/list/',
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            },
            withCredentials: true
          }
        );
        if (res.data.status === 'success') {
          this.rooms = res.data.data.map((c, i) => ({
            id: c.id,
            name: c.name,
            location: c.location,
            number_of_seat: c.number_of_seat,
            is_available: c.is_available,
            is_disable: c.is_disable,
            updated_at: c.updated_at
          }))
        } else {
          this.$message.error(res.data.message || 'Failed to load classrooms')
        }
      } catch (err) {
        console.error(err)
        this.$message.error('Server error fetching classrooms')
      }
    },

    async toggleDisable(row) {
      try {
        const token = localStorage.getItem('token');
        const payload = { id: row.id };
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/classroom/disable/',
          payload,
          {
            headers: { 
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json' 
            } 
          }
        );

        if (res.data.message && res.data.message.includes('successfully')) {
          this.$message({
            message: res.data.message,
            type: 'success',
          });
          await this.fetchRooms();
          this.$emit('room-status-changed');
        } else {
          this.$message({
            message: res.data.message || 'Failed to disable classroom.',
            type: 'error',
          });
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling classroom.');
      }
    },

    async toggleEnable(row) {
      try {
        const token = localStorage.getItem('token');
        const payload = { id: row.id };
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/classroom/enable/',
          payload,
          {
            headers: { 
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json' 
            } 
          }
        );

        if (res.data.message && res.data.message.includes('successfully')) {
          this.$message({
            message: res.data.message,
            type: 'success',
          });
          await this.fetchRooms();
          this.$emit('room-status-changed');
        } else {
          this.$message({
            message: res.data.message || 'Failed to enable classroom.',
            type: 'error',
          });
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling classroom.');
      }
    },

    generateQR(row) {
      this.qrValue = row.id.toString()
      this.showQR = true
    },
    downloadQR() {
      const svg = this.$refs.qrCanvas.$el;
      const svgData = new XMLSerializer().serializeToString(svg);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      
      canvas.width = this.size;
      canvas.height = this.size;
      
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
      this.showQR = false
    }
  },
  mounted() {
    this.fetchRooms()
  }
}
</script>

<style scoped>
.action-bar {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}

.el-dialog__wrapper {
  z-index: 2000 !important;
}

.el-form-item__label {
  font-weight: bold;
}

.el-textarea__inner {
  resize: vertical;
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
.close-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
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
.addRoom {
  width:50%;
}
</style>
