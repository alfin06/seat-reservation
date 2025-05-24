<template>
  <div class="room-management">
    <div class="action-bar">
      <el-button type="primary" @click="showDialog('add')" :loading="loading">
        <i class="el-icon-plus"></i> {{ $t('addRoom') }}
      </el-button>
      <el-input
        v-model="searchQuery"
        :placeholder="$t('searchRoomsPlaceholder')"
        clearable
        style="width: 300px; margin-left: 10px;"
      />
    </div>

    <el-table :data="filteredRooms" border v-loading="loading">
      <el-table-column prop="name" :label="$t('roomName')" sortable />
      <el-table-column prop="capacity" :label="$t('seats')" width="100" />
      <el-table-column :label="$t('status')" width="120">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ $t(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actions')" width="180">
        <template #default="{ row }">
          <el-tag :type="row.is_disable.value ? 'danger' : 'info'">
            {{ row.is_disable.display }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- Updated At -->
      <el-table-column label="Last Updated" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>

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

    <el-dialog 
      :title="dialogTitle" 
      :visible.sync="dialogVisible" 
      width="40%"
      :close-on-click-modal="false"
    >
      <el-form :model="currentRoom" label-width="120px">
        <el-form-item :label="$t('roomName')" required>
          <el-input v-model="currentRoom.name" />
        </el-form-item>
        <el-form-item :label="$t('capacity')">
          <el-input-number v-model="currentRoom.capacity" :min="1" />
        </el-form-item>
        <el-form-item :label="$t('status')">
          <el-switch
            v-model="currentRoom.status"
            active-value="active"
            inactive-value="inactive"
            :active-text="$t('active')"
            :inactive-text="$t('inactive')"
          />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false" :disabled="saving">{{ $t('cancel') }}</el-button>
        <el-button type="primary" @click="saveRoom" :loading="saving">{{ $t('save') }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import QrcodeVue from 'qrcode.vue'
import dayjs from 'dayjs'

export default {
  data() {
    return {
      rooms: [],
      searchQuery: '',
      dialogVisible: false,
      dialogMode: 'add',
      currentRoom: this.getDefaultRoom(),
      loading: false,
      saving: false
    }
  },
  async created() {
    await this.fetchRooms()
  },
  computed: {
    filteredRooms() {
      return this.rooms.filter(room => 
        room.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    dialogTitle() {
      return this.dialogMode === 'add' 
        ? this.$t('addNewRoomTitle') 
        : this.$t('editRoomTitle')
    }
  },
  methods: {
    getDefaultRoom() {
      return { 
        id: null,
        name: '', 
        capacity: 20, 
        status: 'active' 
      }
    },
    async fetchRooms() {
      this.loading = true
      try {
        const response = await adminApi.fetchRoomData()
        this.rooms = response.data || []
      } catch (error) {
        console.error("Room fetch error:", error)
        this.$message.error(this.$t('fetchError'))
      } finally {
        this.loading = false
      }
    },
    showDialog(mode, room = null) {
      this.dialogMode = mode
      this.currentRoom = room ? {...room} : this.getDefaultRoom()
      this.dialogVisible = true
    },
    async saveRoom() {
      this.saving = true
      try {
        if (this.dialogMode === 'add') {
          const response = await adminApi.insertClassroom(this.currentRoom)
          this.rooms.push(response.data)
        } else {
          const response = await adminApi.updateClassroom(this.currentRoom)
          const index = this.rooms.findIndex(r => r.id === this.currentRoom.id)
          if (index !== -1) {
            this.rooms.splice(index, 1, response.data)
          }
        }
        this.$message.success(
          this.dialogMode === 'add' ? this.$t('addSuccess') : this.$t('updateSuccess'))
        this.dialogVisible = false
      } catch (error) {
        console.error("Save error:", error)
        this.$message.error(this.$t('saveError'))
      } finally {
        this.saving = false
      }
    },
    async deleteRoom(room) {
      try {
        await this.$confirm(this.$t('confirmDelete'), this.$t('warning'), {
          confirmButtonText: this.$t('delete'),
          cancelButtonText: this.$t('cancel'),
          type: 'warning'
        })
        this.loading = true
        await adminApi.removeClassroom(room.id)
        this.rooms = this.rooms.filter(r => r.id !== room.id)
        this.$message.success(this.$t('deleteSuccess'))
      } catch (error) {
        if (error !== 'cancel') {
          console.error("Delete error:", error)
          this.$message.error(this.$t('deleteError'))
        }
      } finally {
        this.loading = false
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
    },
    formatDate(dateString) {
      return dayjs(dateString).format('YYYY-MM-DD HH:mm:ss')
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
.el-table .cell {
  text-align: center;
}
.el-tag {
  display: inline-flex;
  justify-content: center;
  min-width: 60px;
}
</style>
