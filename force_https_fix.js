// Script para forzar HTTPS y evitar Mixed Content
// Agregar este script al final del template

(function() {
    'use strict';
    
    console.log('🔧 Force HTTPS Fix iniciado');
    
    // Interceptar todas las llamadas fetch
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        // Si la URL es HTTP y estamos en HTTPS, convertir a HTTPS
        if (typeof url === 'string' && url.startsWith('http://') && window.location.protocol === 'https:') {
            const httpsUrl = url.replace('http://', 'https://');
            console.log('🔄 Convirtiendo URL HTTP a HTTPS:', url, '->', httpsUrl);
            url = httpsUrl;
        }
        
        return originalFetch.call(this, url, options);
    };
    
    // Interceptar XMLHttpRequest también
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
        if (typeof url === 'string' && url.startsWith('http://') && window.location.protocol === 'https:') {
            const httpsUrl = url.replace('http://', 'https://');
            console.log('🔄 Convirtiendo XHR HTTP a HTTPS:', url, '->', httpsUrl);
            url = httpsUrl;
        }
        
        return originalOpen.call(this, method, url, async, user, password);
    };
    
    console.log('✅ Force HTTPS Fix activado');
})();