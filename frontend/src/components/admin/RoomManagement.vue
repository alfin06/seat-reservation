<template>
  <div class="room-management">
    <div class="action-bar">
      <el-button type="primary" @click="showAddRoomForm">
        <i class="el-icon-plus"></i> Add Room
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="Search room..."
        clearable
        style="width: 300px; margin-left: 10px;"
      />
    </div>

    
    <!-- Add Room Dialog -->
    <el-dialog
      title="Add New Room"
      :visible.sync="addRoomDialogVisible"
      width="40%"
    >
      <el-form 
        :model="newRoom" 
        :rules="roomRules" 
        ref="roomForm"
        label-width="120px"
      >
        <el-form-item label="Room Name" prop="name">
          <el-input v-model="newRoom.name" placeholder="e.g., Conference Room A" />
        </el-form-item>

        <el-form-item label="Location" prop="location">
          <el-input v-model="newRoom.location" placeholder="e.g., Building 2, Floor 3" />
        </el-form-item>

        <el-form-item label="Capacity" prop="capacity">
          <el-input-number 
            v-model="newRoom.capacity" 
            :min="1" 
            :max="100"
            placeholder="Number of seats"
          />
        </el-form-item>

        <el-form-item label="Description">
          <el-input
            v-model="newRoom.description"
            type="textarea"
            :rows="2"
            placeholder="Optional room description"
          />
        </el-form-item>
      </el-form>

      <span slot="footer">
        <el-button @click="addRoomDialogVisible = false">Cancel</el-button>
        <el-button 
          type="primary" 
          @click="submitRoomForm"
          :loading="isSubmitting"
        >
          Create Room
        </el-button>
      </span>
    </el-dialog>

    <el-table :data="displayedRooms" border>
      <!-- Name -->
      <el-table-column prop="name" label="Classroom Name" sortable />

      <!-- Location -->
      <el-table-column prop="location" label="Location" />

      <el-table-column prop="number_of_seat" label="Number of Seat" />

      <!-- Availability -->
      <el-table-column label="Available" width="120">
        <template #default="{ row }">
          <el-tag :type="row.is_available.value ? 'success' : 'warning'">
            {{ row.is_available.display }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- Disabled -->
      <el-table-column label="Status" width="120">
        <template #default="{ row }">
          <el-tag :type="row.is_disable.value ? 'danger' : 'info'">
            {{ row.is_disable.display }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- Updated At -->
      <el-table-column prop="updated_at" label="Last Updated" width="180" />

      <!-- Actions -->
      <el-table-column label="Actions" width="200">
        <template #default="{ row }">
          <el-button
            size="mini"
            @click="showDialog('edit', row)"
          >
            Edit
            <i class="el-icon-edit" style="margin-left:4px;"></i>
          </el-button>
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
        </template>
      </el-table-column>
    </el-table>

    <!-- Add / Edit Dialog -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="40%"
    >
      <el-form :model="currentRoom" label-width="120px">
        <el-form-item label="Classroom Name" required>
          <el-input v-model="currentRoom.name" />
        </el-form-item>
        <el-form-item label="Location">
          <el-input v-model="currentRoom.location" />
        </el-form-item>
        <el-form-item label="Available">
          <el-switch
            v-model="currentRoom.is_available.value"
            active-text="Available"
            inactive-text="Reserved"
          />
        </el-form-item>
        <el-form-item label="Disabled">
          <el-switch
            v-model="currentRoom.is_disable.value"
            active-text="Disabled"
            inactive-text="Active"
          />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveRoom">Save</el-button>
      </span>
    </el-dialog>

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

export default {
  data() {
    return {
      addRoomDialogVisible: false,
      isSubmitting: false,
      newRoom: {
        name: '',
        location: '',
        capacity: null,
        description: ''
      },
      roomRules: {
        name: [
          { required: true, message: 'Please enter room name', trigger: 'blur' },
          { min: 3, max: 50, message: 'Length should be 3 to 50', trigger: 'blur' }
        ],
        location: [
          { required: true, message: 'Please enter room location', trigger: 'blur' }
        ],
        capacity: [
          { required: true, message: 'Please enter room capacity', trigger: 'blur' },
          { type: 'number', min: 1, message: 'Capacity must be at least 1', trigger: 'blur' }
        ]
      },

      currentPage: 1,
      pageSize: 15,
      rooms: [],          // fetched from API
      searchQuery: '',
      dialogVisible: false,
      dialogMode: 'add',
      currentRoom: this.getDefaultRoom(),
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
      this.addRoomDialogVisible = true
      this.resetRoomForm()
    },

    resetRoomForm() {
      this.newRoom = {
        name: '',
        location: '',
        capacity: null,
        description: ''
      }
      if (this.$refs.roomForm) {
        this.$refs.roomForm.resetFields()
      }
    },

    async submitRoomForm() {
      this.$refs.roomForm.validate(async (valid) => {
        if (valid) {
          this.isSubmitting = true
          try {
            const response = await axios.post('/api/rooms', {
              name: this.newRoom.name,
              location: this.newRoom.location,
              capacity: this.newRoom.capacity,
              description: this.newRoom.description
            })

            if (response.data.success) {
              this.$message.success('Room created successfully!')
              this.addRoomDialogVisible = false
              // Optionally refresh room list if needed
            }
          } catch (error) {
            console.error('Room creation failed:', error)
            this.$message.error(error.response?.data?.message || 'Failed to create room')
          } finally {
            this.isSubmitting = false
          }
        }
      })
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
        const res = await axios.get('http://127.0.0.1:8000/dashboard/admin/classroom/list/')
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

    showDialog(mode, room = null) {
      this.dialogMode = mode
      this.currentRoom = room
        ? JSON.parse(JSON.stringify(room))
        : this.getDefaultRoom()
      this.dialogVisible = true
    },

    async saveRoom() {
      // stub: wire up to your create/update API as needed
      this.dialogVisible = false
      await this.fetchRooms()
    },

    async toggleDisable(row) {
      // stub: call your disable API
              // stub: call your disable API
      try {
        const payload = { id: row.id };
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/classroom/disable/',
          payload,
        );

        if (res.data.status === 'success') {
          this.$message.success('Classroom status toggled.');
        } else {
          this.$message.error(res.data.message || 'Failed to toggle classroom.');
        }
        
        // refresh list
        await this.fetchRooms();
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling classroom.');
      }
    },

    async toggleEnable(row) {
      // stub: call your disable API
              // stub: call your disable API
      try {
        const payload = { id: row.id};
        const res = await axios.post(
          'http://127.0.0.1:8000/dashboard/admin/classroom/enable/',
          payload
        );

        if (res.data.status === 'success') {
          this.$message.success('Classroom status toggled.');
        } else {
          this.$message.error(res.data.message || 'Failed to toggle classroom.');
        }
        
        // refresh list
        await this.fetchRooms();
      } catch (err) {
        console.error(err);
        this.$message.error('Server error toggling classroom. ');
      }
    },

    async deleteRoom(row) {
      // stub: call your delete API
      await this.fetchRooms()
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
</style>
