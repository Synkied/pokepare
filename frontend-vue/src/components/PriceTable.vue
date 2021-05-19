<template>
  <v-container fluid>
    <v-card outlined>
      <v-data-table
        dark
        dense
        :search="searchQuery"
        :headers="headers"
        :items="orderedPrices"
        :options="tableOptions"
      >
      <template v-slot:top>
        <v-container>
          <v-row>
            <v-col>
              <v-text-field
                v-model="searchQuery"
                clearable
                dense
                label="Search"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-autocomplete
                v-model="selectedWebsites"
                :items="websites"
                clearable
                dense
                chips
                small-chips
                label="Website"
                multiple
              ></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete
                v-model="selectedConditions"
                :items="conditions"
                clearable
                dense
                chips
                small-chips
                label="Condition"
                multiple
              ></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete
                v-model="selectedEditions"
                :items="editions"
                clearable
                dense
                chips
                small-chips
                label="Edition"
                multiple
              ></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete
                v-model="selectedCurrencies"
                :items="currencies"
                clearable
                dense
                chips
                small-chips
                label="Currency"
                multiple
              ></v-autocomplete>
            </v-col>
          </v-row>
        </v-container>
      </template>
      <template v-slot:item.link="{ item }">
        <v-btn icon color="white" :href="item.link" target="_blank">
          <v-icon small>
            launch
          </v-icon>
        </v-btn>
      </template>
      <template v-slot:item.copy_row="{ item }">
        <v-tooltip content-class="copy-tooltip" nudge-right="8" :open-on-click="true" close-delay="200" right>
          <template v-slot:activator="{ on }">
            <v-btn icon color="white" @mouseover="rowCopyTooltipText = 'Copy row'" @click="copyRow(item.product_id); rowCopyTooltipText = 'Copied!'" v-on="on">
              <v-icon small>
                file_copy
              </v-icon>
            </v-btn>
          </template>
          <span>{{ rowCopyTooltipText }}</span>
        </v-tooltip>
      </template>
      <template v-slot:no-data="{ item }">
        No prices found for {{ item.card_unique_id }}.
      </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
/* Imports */
import utils from '@/utils'

/* data, methods, components... declaration */
export default {
  props: ['cards'],
  data () {
    return {
      headers: [
        { text: 'Card id', value: 'card_unique_id' },
        { text: 'Website', value: 'website' },
        { text: 'Condition', value: 'condition' },
        { text: 'Edition', value: 'edition' },
        { text: 'Current Price', value: 'market_price' },
        { text: 'Currency', value: 'currency' },
        { text: 'URL', value: 'link', sortable: false, align: 'end' },
        { text: '', value: 'copy_row', sortable: false, align: 'end', width: '1%' }
      ],
      tableOptions: {
        itemsPerPage: 25
      },
      searchQuery: '',
      selectedWebsites: '',
      selectedConditions: '',
      selectedEditions: '',
      selectedCurrencies: '',
      rowCopyTooltipText: 'Copy row',
      cardsData: []
    }
  },
  title () {
    return `PokePare`
  },
  watch: {
    cards: {
      immediate: true,
      deep: true,
      handler (newVal, oldVal) {
        if (newVal) {
          this.cardsData = newVal
        }
      }
    }
  },
  computed: {
    orderedPrices () {
      let sortedCardsPrices = []
      for (var i = this.cardsData.length - 1; i >= 0; i--) {
        let sortedCardPrices = JSON.parse(JSON.stringify(this.cardsData[i].prices))
        sortedCardPrices = sortedCardPrices.sort((a, b) => {
          return a.market_price - b.market_price
        })
        sortedCardsPrices.push(...sortedCardPrices)
      }
      return sortedCardsPrices
    },
    websites () {
      return this.computeSearchItems('website')
    },
    conditions () {
      return this.computeSearchItems('condition')
    },
    editions () {
      return this.computeSearchItems('edition')
    },
    currencies () {
      return this.computeSearchItems('currency')
    }
  },
  methods: {
    computeSearchItems (itemToGet) {
      let uniqueItems = new Set()
      for (var i = this.cardsData.length - 1; i >= 0; i--) {
        for (var j = this.cardsData[i].prices.length - 1; j >= 0; j--) {
          var item = utils.deepGet(this.cardsData[i].prices[j], itemToGet, '')
          uniqueItems.add(item)
        }
      }
      return Array.from(uniqueItems)
    },
    copyRow (productId) {
      for (var i = this.cardsData.length - 1; i >= 0; i--) {
        for (var j = this.cardsData[i].prices.length - 1; j >= 0; j--) {
          if (this.cardsData[i].prices[j].product_id === productId) {
            this.$clipboard(this.cardsData[i].prices[j])
          }
        }
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-tooltip__content.copy-tooltip {
  border-radius: 0;
  padding: 2px 5px;
  font-size: 12px;
}
</style>
