<template>
  <div class="room-management">
    <div class="action-bar">
      <el-button type="primary" @click="showDialog('add')" :loading="loading">
        <i class="el-icon-plus"></i> Add Room
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="Search rooms..."
        clearable
        style="width: 300px; margin-left: 10px;"
      />
    </div>

    <el-table :data="filteredRooms" border v-loading="loading">
      <el-table-column prop="name" label="Room Name" sortable></el-table-column>
      <el-table-column prop="capacity" label="Seats" width="100"></el-table-column>
      <el-table-column label="Status" width="120">
        <template #default="{row}">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="180">
        <template #default="{row}">
          <el-button 
            size="mini" 
            icon="el-icon-edit" 
            @click="showDialog('edit', row)"
            :disabled="loading"
          />
          <el-button 
            type="danger" 
            size="mini" 
            icon="el-icon-delete" 
            @click="deleteRoom(row)"
            :disabled="loading"
          />
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
        <el-form-item label="Room Name" required>
          <el-input v-model="currentRoom.name"></el-input>
        </el-form-item>
        <el-form-item label="Seats">
          <el-input-number v-model="currentRoom.capacity" :min="1"></el-input-number>
        </el-form-item>
        <el-form-item label="Status">
          <el-switch
            v-model="currentRoom.status"
            active-value="active"
            inactive-value="inactive"
            active-text="Active"
            inactive-text="Inactive"
          />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false" :disabled="saving">Cancel</el-button>
        <el-button type="primary" @click="saveRoom" :loading="saving">Save</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import adminApi from '@/services/adminApi'

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
      return this.dialogMode === 'add' ? 'Add New Room' : 'Edit Room'
    }
  },
  methods: {
    getDefaultRoom() {
      return { 
        id: Date.now(), // Temporary ID for new rooms
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
        this.$message.error('Failed to load rooms')
      } finally {
        this.loading = false
      }
    },
    showDialog(mode, room = null) {
      this.dialogMode = mode
      this.currentRoom = room ? {...room} : this.getDefaultRoom()
      this.dialogVisible = true
      console.log("Editing room:", this.currentRoom) // Debug log
    },
    async saveRoom() {
      this.saving = true
      try {
        if (this.dialogMode === 'add') {
          const response = await adminApi.insertClassroom(this.currentRoom)
          this.rooms.push(response.data)
        } else {
          // Fixed edit logic
          const response = await adminApi.insertClassroom(this.currentRoom)
          const index = this.rooms.findIndex(r => r.id === this.currentRoom.id)
          if (index !== -1) {
            this.rooms.splice(index, 1, response.data)
          }
        }
        this.$message.success(
          this.dialogMode === 'add' ? 'Room added!' : 'Room updated!'
        )
        this.dialogVisible = false
      } catch (error) {
        console.error("Save error:", error)
        this.$message.error('Operation failed')
      } finally {
        this.saving = false
      }
    },
    async deleteRoom(room) {
      try {
        await this.$confirm('Delete this room permanently?', 'Warning', {
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
          type: 'warning'
        })
        this.loading = true
        await adminApi.removeClassroom(room.id)
        this.rooms = this.rooms.filter(r => r.id !== room.id)
        this.$message.success('Room deleted successfully')
      } catch (error) {
        if (error !== 'cancel') {
          console.error("Delete error:", error)
          this.$message.error('Failed to delete room')
        }
      } finally {
        this.loading = false
      }
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
/* Center table content */
.el-table .cell {
  text-align: center;
}
/* Center status tags */
.el-tag {
  display: inline-flex;
  justify-content: center;
  min-width: 60px;
}
</style>