package main

import "testing"

func TestShipUpate(t *testing.T) {
	ship := Ship{direction: 'E'}
	ship.update('R', 90)
	if ship.direction != 'S' {
		t.Errorf("90deg clockwise rotation should be south")
	}

	ship = Ship{direction: 'E'}
	ship.update('R', 180)
	if ship.direction != 'W' {
		t.Errorf("180deg clockwise rotation should be west")
	}

	ship = Ship{direction: 'E'}
	ship.update('R', 270)
	if ship.direction != 'N' {
		t.Errorf("270deg clockwise rotation should be north")
	}

	ship = Ship{direction: 'E'}
	ship.update('R', 360)
	if ship.direction != 'E' {
		t.Errorf("360deg clockwise rotation should be east")
	}

	ship = Ship{direction: 'E'}
	ship.update('R', 450)
	if ship.direction != 'S' {
		t.Errorf("450deg clockwise rotation should be south")
	}

	ship = Ship{direction: 'E'}
	ship.update('R', 540)
	if ship.direction != 'W' {
		t.Errorf("450deg clockwise rotation should be west")
	}

	ship = Ship{direction: 'E'}
	ship.update('L', 90)
	if ship.direction != 'N' {
		t.Errorf("90deg counter-clockwise rotation should be north")
	}

	ship = Ship{direction: 'E'}
	ship.update('L', 180)
	if ship.direction != 'W' {
		t.Errorf("180deg counter-clockwise rotation should be west")
	}

	ship = Ship{direction: 'E'}
	ship.update('L', 270)
	if ship.direction != 'S' {
		t.Errorf("270deg counter-clockwise rotation should be south")
	}

	ship = Ship{direction: 'E'}
	ship.update('L', 360)
	if ship.direction != 'E' {
		t.Errorf("360deg counter-clockwise rotation should be east")
	}

	ship = Ship{direction: 'E'}
	ship.update('L', 450)
	if ship.direction != 'N' {
		t.Errorf("540deg counter-clockwise rotation should be north")
	}

	ship = Ship{direction: 'E'}
	ship.update('L', 540)
	if ship.direction != 'W' {
		t.Errorf("540deg counter-clockwise rotation should be west")
	}
}
