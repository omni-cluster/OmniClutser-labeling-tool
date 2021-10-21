import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Label from '@/components/Label'
import Check from '@/components/Check'
// eslint-disable-next-line camelcase
import Check_z from '../components/Check_z'
// eslint-disable-next-line camelcase
import Check_reconstruct from '../components/Check_reconstruct'

Vue.use(Router)
const routers = [
  {
    path: '/',
    name: 'Index',
    component: Index
  },
  {
    path: '/label',
    name: 'Label',
    component: Label
  },
  {
    path: '/check',
    name: 'Check',
    component: Check
  },
  {
    path: '/check_z',
    name: 'CheckZ',
    component: Check_z
  },
  {
    path: '/check_reconstruct',
    name: 'CheckReconstruct',
    component: Check_reconstruct
  }
]
export default routers
