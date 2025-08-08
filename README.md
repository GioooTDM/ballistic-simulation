# Intercettazione balistica

![Immagine](/img/hero_text.jpg){ width=75% }

## 1 · Descrizione del problema
Un missile attaccante, chiamato **bersaglio**, parte da destra verso sinistra con moto parabolico.  
Un missile **intercettore** può essere lanciato dalla difesa con **modulo di velocità fissato** \(v_0\).  

> **Obiettivo:** stabilire, nell’istante corrente, se esiste una traiettoria che consenta all’intercettore di colpire il bersaglio; in caso positivo determinare angolo di lancio \( \theta \), tempo d’impatto \( t_{\text{hit}} \) e componenti di velocità \( (v_x,v_y) \).

---

## 2 · Legenda

| Simbolo | Significato | 
|---------|-------------|
| \(x_0,\;y_0\) | punto di lancio dell’intercettore **I** | 
| \(x_{B0},\;y_{B0}\) | posizione attuale del bersaglio **B** | 
| \(v_{Bx},\;v_{By}\) | componenti della velocità del bersaglio (misurate nell'istante in cui l’intercettore viene lanciato) | 
| \(v_0\) | **modulo fissato** della velocità d’uscita dell’intercettore | 
| \(\theta\) | angolo di lancio dell'intercettore misurato dall’asse orizzontale verso l’alto | 
| \(g\) | gravità ( \(g>0\) verso il basso ) | 
| \(t\) | tempo trascorso dal lancio | 
| \(\Delta x(t),\,\Delta y(t)\) | differenze di posizione B–I all’istante \(t\) |

---

## 3 · Convenzione assi

* Nel **sistema fisico** l’asse \(y\) cresce verso l’alto.  
  Equazioni verticali: \(\;y(t)=y_0 + v_y t - \frac12 g t^{2}\).

* In **Pygame** l’asse \(y\) cresce verso il basso.  
  Per coerenza col codice useremo la convenzione di Pygame:  
  \(\;y(t)=y_0 + v_y t + \frac12 g t^{2}\).

---

## 4 · Equazioni di moto nel sistema Pygame

### Bersaglio **B**
\[
\boxed{\;
\begin{aligned}
x_B(t) &= x_{B0} + v_{Bx}\,t \\[4pt]
y_B(t) &= y_{B0} + v_{By}\,t + \tfrac12\,g\,t^{2}
\end{aligned}}
\]

### Intercettore **I**
\[
\boxed{\;
\begin{aligned}
x_I(t) &= x_0 + v_0\cos\theta\,t \\[4pt]
y_I(t) &= y_0 - v_0\sin\theta\,t + \tfrac12\,g\,t^{2}
\end{aligned}}
\tag{1}
\]

*(il termine - \(v_0\sin\theta\,t\) indica uno sparo “verso l’alto” nel sistema Pygame).*

---

## 5 · Condizione di impatto

Affinché l’intercettore **I** colpisca il bersaglio **B** nello stesso istante _t_ le loro coordinate devono coincidere:

\[
\begin{aligned}
x_B(t) &= x_I(t) \\[4pt]
y_B(t) &= y_I(t)
\end{aligned}
\tag{2}
\]


Sostituiamo (1) in (2):

\[
\begin{aligned}
x_B(t) &= x_0 + v_0\cos\theta\,t \\[4pt]
y_B(t) &= y_0 - v_0\sin\theta\,t + \tfrac12\,g\,t^{2}
\end{aligned}
\]


Sapendo che:


\[
\begin{aligned}
v_0\cos\theta\ &= v_x \\
-v_0\sin\theta\ &= v_y
\end{aligned}
\]

Otteniamo:

\[
\begin{aligned}
v_x &= \dfrac{x_B(t) - x_0}{t} \\[4pt]
v_y &= \dfrac{y_B(t) - y_0}{t}-\dfrac{1}{2}gt
\end{aligned}
\]



---

## 6 · Componenti “richieste” per colpire in tempo \(t\)
Definiamo gli scarti di posizione

\[
\Delta x(t)=x_B(t)-x_0,\qquad
\Delta y(t)=y_B(t)-y_0
\]

Le componenti richieste $v_x^∗$ e $v_y^*$​ rappresentano la velocità che l’intercettore dovrebbe avere al momento del lancio per colpire esattamente il bersaglio in un tempo $t$:

\[
\boxed{\,v_x^{\ast}= \dfrac{\Delta x(t)}{t}},\qquad
\boxed{\,v_y^{\ast}= \dfrac{\Delta y(t)}{t}-\dfrac{1}{2}\,g\,t\,}
\tag{3}
\]

---

## 7 · Vincolo di modulo fisso e funzione $f(t)$

Poiché l’intercettore può partire solo con un modulo di velocità fissato $v_0$, le componenti richieste devono soddisfare:

\[
\sqrt{(v_x^{\ast})^{2}+(v_y^{\ast})^{2}} = v_0
\;\;\Longrightarrow\;\;
(v_x^{\ast})^{2} + (v_y^{\ast})^{2} - v_0^{2} = 0
\tag{4}
\]

Sostituiamo (3) in (4):

\[
\left(\frac{\Delta x}{t}\right)^{\!2}
+\left(\frac{\Delta y}{t}-\frac12 g t\right)^{\!2}
-v_0^{2}=0
\]

Moltiplichiamo per \(t^{2}\):

\[
(\Delta x)^{2} + \Bigl(\Delta y - \tfrac{1}{2}gt^2\Bigr)^{2}-v_0^{2}t^{2}=0
\]

<!-- \[
\Delta x^{2}+\Delta y^{2}-\Delta y\,g\,t^{2}
+\tfrac14 g^{2}t^{4}-v_0^{2}t^{2}=0
\] -->

poniamo

\[
\boxed{\,f(t)=
(\Delta x)^{2}
+\Bigl(\Delta y -\tfrac12 g t^{2}\Bigr)^{2}
-\;v_0^{2}t^{2}\,}=0
\]

\(f(t)\) è una funzione continua; trovare il tempo di impatto equivale a cercare una radice positiva di \(f(t)\).

---

## 8 · Ricerca numerica della radice

1. **Scansione iniziale** su \(t\in[t_{\min},t_{\max}]\) con passo \(\Delta t\) per individuare un intervallo \([a,b]\) con \(f(a)\,f(b)<0\).
2. **Bisezione** su \([a,b]\):
   * calcolo del medio \(m\)
   * sostituzione dell’intervallo che contiene il cambio di segno
   * iterazione finché \(|f(m)|<\varepsilon\).

---

## 9 · Ricostruzione di traiettoria e angolo

Con \(t_{\text{hit}}\) trovato:

\[
\begin{aligned}
v_x &= \frac{\Delta x(t_{\text{hit}})}{t_{\text{hit}}},\\[6pt]
v_y &= \frac{\Delta y(t_{\text{hit}})}{t_{\text{hit}}}-\frac12 g\,t_{\text{hit}},\\[6pt]
\theta &= \operatorname{atan2}(-v_y,\;v_x)\;.
\end{aligned}
\]

---

## 10 · Algoritmo finale (pseudo-codice)

```text
def intercept_fixed_speed(...):
    for t in [t_min : Δt : t_max]:
        if f(t) cambia segno ⇒ salvo [a,b] e interrompo
    if nessun intervallo: return None
    t_hit = bisezione(f, a, b, ε)
    vx = Δx(t_hit) / t_hit
    vy = Δy(t_hit) / t_hit - 0.5*g*t_hit
    angle = atan2(-vy, vx)
    return angle, t_hit, vx, vy
```