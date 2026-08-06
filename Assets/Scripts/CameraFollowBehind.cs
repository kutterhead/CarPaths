using UnityEngine;

// Cámara de persecución que se mantiene DETRÁS del vehículo (según su orientación)
// y lo enfoca. Versión mejorada de CameraFollow que sí gira con el coche.
public class CameraFollowBehind : MonoBehaviour {

	[Header("Objetivo")]
	public Transform carTransform;

	[Header("Posición detrás del coche")]
	[Tooltip("Distancia por detrás del coche (en metros).")]
	public float distance = 6f;
	[Tooltip("Altura de la cámara sobre el coche (en metros).")]
	public float height = 2.5f;

	[Header("Suavizado")]
	[Range(1, 20)]
	public float followSpeed = 5f;
	[Range(1, 20)]
	public float lookSpeed = 8f;

	[Tooltip("Punto al que mira la cámara, por encima del pivote del coche.")]
	public float lookAtHeight = 1f;

	void Start() {
		if (carTransform == null) {
			Debug.LogWarning("CameraFollowBehind: 'carTransform' no está asignado.", this);
			return;
		}
		// Colocar la cámara ya en su sitio para evitar un salto inicial.
		transform.position = GetTargetPosition();
		transform.rotation = GetLookRotation();
	}

	void FixedUpdate() {
		if (carTransform == null) return;

		// Mover detrás del coche, suavizado.
		transform.position = Vector3.Lerp(transform.position, GetTargetPosition(), followSpeed * Time.fixedDeltaTime);

		// Mirar hacia el coche, suavizado.
		transform.rotation = Quaternion.Slerp(transform.rotation, GetLookRotation(), lookSpeed * Time.fixedDeltaTime);
	}

	Vector3 GetTargetPosition() {
		// Detrás según la orientación del coche + altura.
		return carTransform.position - carTransform.forward * distance + Vector3.up * height;
	}

	Quaternion GetLookRotation() {
		Vector3 lookTarget = carTransform.position + Vector3.up * lookAtHeight;
		Vector3 dir = lookTarget - transform.position;
		if (dir.sqrMagnitude < 0.0001f) return transform.rotation;
		return Quaternion.LookRotation(dir, Vector3.up);
	}
}
