<!-- <script setup lang="ts">
import DecreaseButton from './DecreaseButton.vue';
import IncreaseButton from './IncreaseButton.vue';
import PrintStatusButton from './PrintStatusButton.vue';
import RemoveButton from './RemoveButton.vue';
</script>

<template>
    <div style="height: 2.5rem; display: flex; gap: 0.25rem; margin-bottom: 0.25rem;">
        <PrintStatusButton />
    </div>
    <div style="margin-top: 0.25rem;">
        <table>
            <thead>
                <tr>
                    <th style="width: 1rem;">#</th>
                    <th>Ürün</th>
                    <th style="width: 5rem;">Birim Fiyat</th>
                    <th style="width: 8rem;">Adet</th>
                    <th style="width: 5rem;">Tutar</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="$order.obj.items.length > 0" v-for="(item, index) in $order.obj.items">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.product }}</td>
                    <td>{{ item.unit_price }}</td>
                    <td>
                        <div
                            style="display: flex; justify-content: start; gap: 0.25rem; flex: 0 0 auto; min-width: 0; flex-grow: 0;">
                            <DecreaseButton :item-id="item.id" />
                            <input style="width: 1.5rem; padding: 0.5rem 0 0.5rem 0.5rem;" type="number"
                                v-model="item.quantity" disabled>
                            <IncreaseButton :item-id="item.id" />
                            <RemoveButton :item-id="item.id" />
                        </div>
                    </td>
                    <td style="text-align: right;">{{ item.amount }} TL</td>
                </tr>
                <tr v-if="$order.obj.items.length > 0">
                    <td style="padding: 16px 8px;" colspan="4">
                        <strong>Toplam</strong>
                    </td>
                    <td style="text-align: right;">
                        <strong>{{ $order.obj.total }} TL</strong>
                    </td>
                </tr>
                <tr v-else>
                    <td colspan="5" style="text-align: center;">Bu masanın henüz bir siparişi yok.</td>
                </tr>
            </tbody>
        </table>
    </div>
</template> -->