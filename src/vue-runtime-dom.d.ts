import type { useOrderData } from './stores/order';
import { useProcess } from './stores/process'

declare module 'vue' {
  interface ComponentCustomProperties {
    $process: ReturnType<typeof useProcess>;
  }

  interface ComponentCustomProperties {
    $order: ReturnType<typeof useOrderData>;
  }
}