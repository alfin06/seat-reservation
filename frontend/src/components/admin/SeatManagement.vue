<template>
  <div class="seat-management">
    <div class="action-bar">
      <el-input
        v-model="searchQuery"
        placeholder="Search seat..."
        clearable
        style="width: 300px; margin-left: 10px;"
      />
    </div>

    <el-table :data="displayedSeats" border>
      <el-table-column prop="name" label="Seat Name" sortable />
      <el-table-column prop="location" label="Location" />
      <el-table-column prop="classroom" label="Classroom" width="120"/>

      <!-- Availability -->
      <el-table-column label="Available" width="90">
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

      <el-table-column prop="updated_at" label="Last Updated" width="180" />
      
      <el-table-column label="Actions" width="180">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              type="warning"
              size="mini"
              @click="toggleEnable(row)"
            >
              Enable
            </el-button>
            <el-button
              type="danger"
              size="mini"
              @click="toggleDisable(row)"
            >
              Disable
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
      <el-table-column label="QR Code" width="140">
        <template #default="{ row }">
          <el-button
            size="mini"
            @click="generateQR(row)"
            class="open-btn"
          >
            Generate QR
          </el-button>
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

    <div class="pagination">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="filteredSeats.length"
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
      currentPage: 1,
      pageSize: 15,
      seats: [],
      searchQuery: '',
      showQR: false,
      qrValue: '',
      size: 200           // QR code pixel size
    }
  },
  computed: {
    filteredSeats() {
      return this.seats.filter(r =>
        r.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    displayedSeats() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredSeats.slice(start, start + this.pageSize)
    }
  },
  methods: {
    handlePageChange(newPage) {
      this.currentPage = newPage
    },

    getDefaultSeat() {
      return {
        id: null,
        name: '',
        location: '',
        classroom: '',
        is_available: { value: 1, display: 'Available' },
        is_disable: { value: 0, display: 'Active' },
        updated_at: ''
      }
    },

    async fetchSeats() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(
          'http://127.0.0.1:8000/dashboard/admin/seats/list/',
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json' 
            }
          }
        )
        if (res.data.status === 'success') {
          this.seats = res.data.data.map((c, i) => ({
            id: c.id,
            name: 'Seat ' + c.id + '-' + c.location,
            location: c.location,
            classroom: c.classroom,
            is_available: c.is_available,
            is_disable: c.is_disable, 
            updated_at: c.update_at
          }))
        } else {
          this.$message.error(res.data.message || 'Failed to load seats')
        }
      } catch (err) {
        console.error(err)
        this.$message.error('Server error fetching seats')
      }
    },

    async toggleDisable(row) {
      try {
        const token = localStorage.getItem('token');
        const payload = { id: row.id };
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/seats/disable/',
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
          await this.fetchSeats();
        } else {
          this.$message({
            message: res.data.message || 'Failed to disable seat.',
            type: 'error',
          });
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling seat.');
      }
    },

    async toggleEnable(row) {
      try {
        const token = localStorage.getItem('token');
        const payload = { id: row.id };
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/seats/enable/',
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
          await this.fetchSeats();
        } else {
          this.$message({
            message: res.data.message || 'Failed to enable seat.',
            type: 'error',
          });
        }
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling seat.');
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
      
      // Set canvas size to match QR code
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
    this.fetchSeats()
  },
  watch: {
    // Watch for room status changes and refresh seats
    '$parent.activeTab': {
      handler(newTab) {
        if (newTab === 'seats') {
          this.fetchSeats();
        }
      },
      immediate: true
    }
  }
}
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
</style>
