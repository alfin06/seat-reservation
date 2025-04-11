<template>
    <div class="room-management">
      <div class="action-bar">
        <el-button type="primary" @click="showDialog('add')">
          <i class="el-icon-plus"></i> Add Room
        </el-button>
        <el-input
          v-model="searchQuery"
          placeholder="Search rooms..."
          clearable
          style="width: 300px; margin-left: 10px;"
        />
      </div>
  
      <el-table :data="filteredRooms" border>
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
            />
            <el-button 
              type="danger" 
              size="mini" 
              icon="el-icon-delete" 
              @click="deleteRoom(row)"
            />
          </template>
        </el-table-column>
      </el-table>
  
      <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="40%">
        <el-form :model="currentRoom" label-width="120px">
          <el-form-item label="Room Name" required>
            <el-input v-model="currentRoom.name"></el-input>
          </el-form-item>
          <el-form-item label="Capacity">
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
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="saveRoom">Save</el-button>
        </span>
      </el-dialog>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        rooms: [
          { id: 1, name: 'Library West', capacity: 30, status: 'active' },
          { id: 2, name: 'Quiet Study A', capacity: 20, status: 'active' }
        ],
        searchQuery: '',
        dialogVisible: false,
        dialogMode: 'add',
        currentRoom: this.getDefaultRoom()
      }
    },
    computed: {
      filteredRooms() {
        return this.rooms.filter(room => 
          room.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        ) // Fixed: Added closing parenthesis
      },
      dialogTitle() {
        return this.dialogMode === 'add' ? 'Add New Room' : 'Edit Room'
      }
    },
    methods: {
      getDefaultRoom() {
        return { id: null, name: '', capacity: 20, status: 'active' }
      },
      showDialog(mode, room = null) {
        this.dialogMode = mode
        this.currentRoom = room ? {...room} : this.getDefaultRoom()
        this.dialogVisible = true
      },
      saveRoom() {
        if (this.dialogMode === 'add') {
          this.rooms.push({...this.currentRoom, id: Date.now()})
        } else {
          const index = this.rooms.findIndex(r => r.id === this.currentRoom.id)
          if (index !== -1) this.rooms.splice(index, 1, this.currentRoom)
        }
        this.dialogVisible = false
      },
      deleteRoom(room) {
        this.$confirm('Delete this room permanently?', 'Warning', {
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          this.rooms = this.rooms.filter(r => r.id !== room.id)
        })
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
  </style>