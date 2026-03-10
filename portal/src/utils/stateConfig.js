/**
 * Configuración de badge para el estado de conservación de un sitio.
 *
 * @param {string} state - Estado de conservación ('Bueno', 'Regular', 'Malo')
 * @returns {{ classes: string, icon: string }} Clases CSS e icono Bootstrap
 */
export function getStateConfig(state) {
  const configMap = {
    Bueno: {
      classes: 'badge bg-success text-white',
      icon: 'bi bi-check-circle-fill',
    },
    Regular: {
      classes: 'badge bg-warning text-dark',
      icon: 'bi bi-exclamation-triangle-fill',
    },
    Malo: {
      classes: 'badge bg-danger text-white',
      icon: 'bi bi-x-circle-fill',
    },
  }

  return (
    configMap[state] || {
      classes: 'badge bg-secondary text-white',
      icon: 'bi bi-question-circle-fill',
    }
  )
}
