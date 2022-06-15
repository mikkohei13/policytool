import {unref} from 'vue'

export const PACK_STATUS = {
    COMPLETE: 'complete',
    INCOMPLETE: 'incomplete',
    NOT_STARTED: 'not_started',
}

export const calcPackStatus = (pack) => {
    pack = unref(pack)
    if (pack['answered'] === 0) {
        return PACK_STATUS.NOT_STARTED
    } else if (pack['answered'] === pack['size']) {
        return PACK_STATUS.COMPLETE
    } else {
        return PACK_STATUS.INCOMPLETE
    }
}
