# 🔧 Solución al Error 403: Permisos de Search Console

## ❌ Error Recibido

```
Error HTTP 403: User does not have sufficient permission for site 'https://directoriodearte.com'
```

---

## 🎯 SOLUCIÓN RÁPIDA

### ✅ **Paso 1: Ver tus sitios disponibles**

1. **Reinicia la aplicación:**
   ```bash
   python run_gui.py
   ```

2. **Ve a la pestaña:** `🔍 Search Console`

3. **Clic en el botón:** `🌐 Ver Mis Sitios en Search Console`

4. **Verás una lista** de todos los sitios a los que tienes acceso

5. **Copia la URL exacta** del sitio que quieres usar

---

### ✅ **Paso 2: Actualizar tu proyecto**

1. **Ve a:** `🏢 Proyectos`

2. **Selecciona tu proyecto** en la tabla

3. **Clic en:** `✏️ Editar Proyecto`

4. **En "URL de Search Console":** Pega la URL EXACTA que copiaste

5. **Guarda los cambios**

---

### ✅ **Paso 3: Intentar nuevamente**

1. **Vuelve a:** `🔍 Search Console`

2. **Selecciona el proyecto** actualizado

3. **Clic en:** `🔄 Obtener Keywords`

4. **¡Debería funcionar!** 🎉

---

## 🔍 CAUSAS DEL ERROR 403

### **1. Cuenta Incorrecta**

**Problema:** Te autenticaste con una cuenta de Google diferente a la que tiene acceso al sitio.

**Solución:**
1. Ve a `⚙️ Configuración` → `Google Search Console`
2. Clic en `🔌 Desconectar`
3. Vuelve a autenticarte con la cuenta correcta (la que tiene acceso en https://search.google.com/search-console)

### **2. Sitio No Verificado**

**Problema:** El sitio `https://directoriodearte.com` no está verificado en Search Console con tu cuenta.

**Solución:**
1. Ve a https://search.google.com/search-console
2. Agrega y verifica el sitio
3. Espera 24-48 horas para que los datos se sincronicen
4. Vuelve a intentar en la aplicación

### **3. URL No Coincide Exactamente**

**Problema:** La URL que configuraste no coincide exactamente con la de Search Console.

**Ejemplos de diferencias:**
- `http://directoriodearte.com` vs `https://directoriodearte.com` (protocolo)
- `https://directoriodearte.com` vs `https://directoriodearte.com/` (trailing slash)
- `https://directoriodearte.com` vs `https://www.directoriodearte.com` (www)

**Solución:**
Usa el botón `🌐 Ver Mis Sitios` para copiar la URL exacta.

### **4. Permisos Insuficientes**

**Problema:** Tu cuenta solo tiene permisos de lectura limitados o restringidos.

**Niveles de permiso necesarios:**
- ✅ **Propietario** (OWNER) - Acceso completo
- ✅ **Propietario completo** (FULL_USER) - Funciona
- ⚠️ **Usuario restringido** (RESTRICTED_USER) - Puede tener problemas
- ❌ **Sin permisos** - No funciona

**Solución:**
Pídele al propietario del sitio que te otorgue permisos de "Propietario completo" en Search Console.

---

## 📋 VERIFICAR ACCESO EN SEARCH CONSOLE

### **Opción 1: Desde el navegador**

1. Ve a https://search.google.com/search-console
2. Asegúrate de estar con la cuenta correcta (arriba a la derecha)
3. Deberías ver `https://directoriodearte.com` en la lista
4. Haz clic en el sitio
5. Si puedes ver datos, tienes acceso ✅

### **Opción 2: Desde la aplicación**

1. Ve a `🔍 Search Console`
2. Clic en `🌐 Ver Mis Sitios en Search Console`
3. Si el sitio aparece en la lista, tienes acceso ✅
4. Si NO aparece, necesitas verificarlo o pedir permisos

---

## 🆘 PASOS PARA AGREGAR UN SITIO NUEVO

### **Si eres propietario del dominio:**

1. **Ve a Search Console:**
   https://search.google.com/search-console

2. **Agregar propiedad:**
   - Clic en "Agregar propiedad"
   - Elige "Prefijo de URL"
   - Ingresa: `https://directoriodearte.com/`

3. **Verificar propiedad:**
   - Método recomendado: **Archivo HTML**
   - Descarga el archivo
   - Súbelo a tu servidor en la raíz del sitio
   - Verifica

4. **Esperar datos:**
   - Los primeros datos aparecen en 24-48 horas
   - Datos históricos pueden tardar hasta 7 días

5. **Volver a la aplicación:**
   - Usa el botón `🌐 Ver Mis Sitios`
   - Copia la URL exacta
   - Actualiza tu proyecto

### **Si NO eres propietario:**

1. **Contacta al propietario del sitio**

2. **Pídele que te agregue:**
   - En Search Console → Configuración → Usuarios y permisos
   - Agregar usuario
   - Tu email de Google
   - Permisos: **Propietario completo** o **Completo**

3. **Aceptar invitación:**
   - Revisa tu email
   - Acepta la invitación
   - Ve a Search Console para confirmar acceso

4. **Usar la aplicación:**
   - Clic en `🌐 Ver Mis Sitios`
   - El sitio debería aparecer ahora

---

## 🔄 CAMBIAR DE CUENTA

Si necesitas usar otra cuenta de Google:

1. **Desconectar cuenta actual:**
   ```
   ⚙️ Configuración → Google Search Console → 🔌 Desconectar
   ```

2. **Volver a autenticar:**
   ```
   🔐 Autenticar con Google
   ```

3. **IMPORTANTE:** En el navegador, asegúrate de:
   - Estar con la cuenta correcta ANTES de aceptar
   - Si hay múltiples cuentas, selecciona la correcta
   - Puedes usar modo incógnito para evitar confusiones

4. **Verificar:**
   ```
   🔍 Search Console → 🌐 Ver Mis Sitios
   ```

---

## 📞 RECURSOS ADICIONALES

### **Google Search Console**
- Inicio: https://search.google.com/search-console
- Ayuda: https://support.google.com/webmasters
- Verificación: https://support.google.com/webmasters/answer/9008080

### **Permisos y Usuarios**
- Gestión de usuarios: https://support.google.com/webmasters/answer/2451999
- Niveles de permiso: https://support.google.com/webmasters/answer/7687615

---

## ✅ CHECKLIST DE SOLUCIÓN

- [ ] He autenticado con la cuenta correcta de Google
- [ ] El sitio está verificado en Search Console
- [ ] He usado el botón "🌐 Ver Mis Sitios" para ver URLs disponibles
- [ ] He copiado la URL EXACTA (con protocolo, con/sin www, con/sin slash)
- [ ] He actualizado la URL en la configuración del proyecto
- [ ] Tengo permisos de "Propietario" o "Completo" en el sitio
- [ ] Han pasado al menos 24 horas desde la verificación del sitio
- [ ] He intentado obtener keywords nuevamente

---

**Si después de seguir todos estos pasos aún tienes problemas, revisa los logs en `logs/scraper.log` para más detalles del error.**
