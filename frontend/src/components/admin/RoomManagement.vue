<template>
  <div class="room-management">
    <div class="action-bar">
      <el-button type="primary" @click="showDialog('add')">
        <i class="el-icon-plus"></i> {{ $t('addRoom') }}
      </el-button>
      <el-input
        v-model="searchQuery"
        :placeholder="$t('searchRoomsPlaceholder')"
        clearable
        style="width: 300px; margin-left: 10px;"
      />
    </div>

    <el-table :data="filteredRooms" border>
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
        <el-button @click="dialogVisible = false">{{ $t('cancel') }}</el-button>
        <el-button type="primary" @click="saveRoom">{{ $t('save') }}</el-button>
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
      return { id: null, name: '', capacity: 20, status: 'active' }
    },
    showDialog(mode, room = null) {
      this.dialogMode = mode
      this.currentRoom = room ? { ...room } : this.getDefaultRoom()
      this.dialogVisible = true
    },
    saveRoom() {
      if (this.dialogMode === 'add') {
        this.rooms.push({ ...this.currentRoom, id: Date.now() })
      } else {
        const index = this.rooms.findIndex(r => r.id === this.currentRoom.id)
        if (index !== -1) this.rooms.splice(index, 1, this.currentRoom)
      }
      this.dialogVisible = false
    },
    deleteRoom(room) {
      this.$confirm(this.$t('confirmDelete'), this.$t('warning'), {
        confirmButtonText: this.$t('delete'),
        cancelButtonText: this.$t('cancel'),
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
