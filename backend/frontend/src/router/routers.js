import Main from '@/components/main'
import parentView from '@/components/parent-view'

/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  title: { String|Number|Function }
 *         显示在侧边栏、面包屑和标签栏的文字
 *         使用'{{ 多语言字段 }}'形式结合多语言使用，例子看多语言的路由配置;
 *         可以传入一个回调函数，参数是当前路由对象，例子看动态路由和带参路由
 *  hideInBread: (false) 设为true后此级路由将不会出现在面包屑中，示例看QQ群路由配置
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面在切换标签后不会缓存，如果需要缓存，无需设置这个字段，而且需要设置页面组件name属性和路由配置的name一致
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 *  beforeCloseName: (-) 设置该字段，则在关闭当前tab页时会去'@/router/before-close.js'里寻找该字段名对应的方法，作为关闭前的钩子函数
 * }
 */

export default [
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login - 登录',
      hideInMenu: true
    },
    component: () => import('@/view/login/login.vue')
  },
  {
    path: '/',
    name: '_home',
    redirect: '/home',
    component: Main,
    meta: {
      hideInMenu: true,
      notCache: true
    },
    children: [
      {
        path: '/home',
        name: 'home',
        meta: {
          hideInMenu: true,
          title: '首页',
          notCache: true,
          icon: 'md-home'
        },
        component: () => import('@/view/single-page/home')
      }
    ]
  },
  {
    path: '/outline',
    name: 'outline',
    component: Main,
    meta: {
      hideInBread: true,
      hideInMenu: true,
    },
    children: [
      {
        path: 'outline_view',
        name: 'outline_view',
        meta: {
          title: '设备概览'
        },
        component: () => import('@/view/outline/outline.vue')
      }
    ]
  },
  {
    path: '/gateway',
    name: 'gateway',
    component: Main,
    meta: {
      icon: 'md-menu',
      title: '网关配置'
    },
    children: [
      {
        path: 'gateway_config',
        name: 'gateway_config',
        meta: {
          title: '网关设备管理'
        },
        component: () => import('@/view/gateway/gateway.vue')
      },
      {
        path: 'mqtt_config',
        name: 'mqtt_config',
        meta: {
          title: 'MQTT传输配置'
        },
        component: () => import('@/view/gateway/mqtt_config.vue')
      },
      {
        path: 'mqtt_topic',
        name: 'mqtt_topic',
        meta: {
          title: 'MQTT主题配置'
        },
        component: () => import('@/view/gateway/mqtt_topic.vue')
      }
    ]
  },
  {
    path: '/device',
    name: 'device',
    component: Main,
    meta: {
      hideInBread: true
    },
    
    children: [
      {
        path: 'device_manage',
        name: '_device_manage',
        meta: {
          icon: 'logo-buffer',
          title: '设备管理',
          hideInBread: false
        },
        redirect: '/device/device_manage/show_list',
        component: () => import('@/view/device/device.vue'),
        children: [
            {
              path: 'show_list',
              name: 'device_manage',
              meta: {
                title: '子设备管理',
                hideInBread: true,
                notCache: true,
              },
              component: () => import('@/view/device/show_list.vue')
            },
            {
              path: 'add_tcp',
              name: 'add_tcp',
              meta: {
                hideInBread: true,
                hideInMenu: true,
                notCache: true,
              },
              component: () => import('@/view/device/TCP_device.vue')
            },
            {
              path: 'add_rtu',
              name: 'add_rtu',
              meta: {
                hideInBread: false,
                hideInMenu: true,
                notCache: true,
              },
              component: () => import('@/view/device/RTU_device.vue')
            }
        ]
      },

    ]
  },
  {
    path: '/task',
    name: 'task',
    component: Main,
    meta: {
      hideInBread: true
    },
    children: [
      {
        path: 'program',
        name: 'program',
        meta: {
          icon: 'md-cloud-upload',
          title: '采集任务',
          // notCache: true,
        },
        component: () => import('@/view/task/task.vue')
      },
      {
        path: 'sub_task/:task_name',
        name: 'sub_task',
        meta: {
          icon: 'md-cloud-upload',
          title: '采集子任务',
          hideInMenu: true,
          hideInBread: true,
          notCache: true,
        },
        component: () => import('@/view/task/sub_task.vue')
      }
    ],
  },
  {
    path: '',
    name: 'doc',
    meta: {
      title: '文档',
      href: 'https://lison16.github.io/iview-admin-doc/#/',
      icon: 'ios-book'
    }
  },
  {
    path: '/message',
    name: 'message',
    component: Main,
    meta: {
      hideInBread: true,
      hideInMenu: true
    },
    children: [
      {
        path: 'message_page',
        name: 'message_page',
        meta: {
          icon: 'md-notifications',
          title: '消息中心'
        },
        component: () => import('@/view/single-page/message/index.vue')
      }
    ]
  },
  {
    path: '/components',
    name: 'components',
    meta: {
      icon: 'logo-buffer',
      title: '组件'
    },
    component: Main,
  },
  {
    path: '/error_store',
    name: 'error_store',
    meta: {
      hideInBread: true
    },
    component: Main,
    children: [
      {
        path: 'error_store_page',
        name: 'error_store_page',
        meta: {
          icon: 'ios-bug',
          title: '错误收集'
        },
        component: () => import('@/view/error-store/error-store.vue')
      }
    ]
  },
  {
    path: '/error_logger',
    name: 'error_logger',
    meta: {
      hideInBread: true,
      hideInMenu: true
    },
    component: Main,
    children: [
      {
        path: 'error_logger_page',
        name: 'error_logger_page',
        meta: {
          icon: 'ios-bug',
          title: '错误收集'
        },
        component: () => import('@/view/single-page/error-logger.vue')
      }
    ]
  },
  {
    path: '/argu',
    name: 'argu',
    meta: {
      hideInMenu: true
    },
    component: Main,
    children: [
      {
        path: 'params/:id',
        name: 'params',
        meta: {
          icon: 'md-flower',
          title: route => `{{ params }}-${route.params.id}`,
          notCache: true,
          beforeCloseName: 'before_close_normal'
        },
        component: () => import('@/view/argu-page/params.vue')
      },
      {
        path: 'query',
        name: 'query',
        meta: {
          icon: 'md-flower',
          title: route => `{{ query }}-${route.query.id}`,
          notCache: true
        },
        component: () => import('@/view/argu-page/query.vue')
      }
    ]
  },
  {
    path: '/401',
    name: 'error_401',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/401.vue')
  },
  {
    path: '/500',
    name: 'error_500',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/500.vue')
  },
  {
    path: '*',
    name: 'error_404',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/404.vue')
  }
]
