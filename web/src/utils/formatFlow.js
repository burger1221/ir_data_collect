export function formatFlow(flowData) {
  let formatted = 0
  if (flowData === 'NULL' || flowData === undefined || flowData === '') {
    formatted = '-'
  } else if (flowData > (1024 * 1024 * 1024)) {
    formatted = (flowData / (1024 * 1024 * 1024)).toFixed(0) + 'GB'
  } else if (flowData > (1024 * 1024)) {
    formatted = (flowData / (1024 * 1024)).toFixed(0) + 'MB'
  } else if (flowData > 1024) {
    formatted = (flowData / 1024).toFixed(0) + 'KB'
  } else {
    formatted = flowData.toFixed(0) + 'Bytes'
  }
  return formatted
}
